"""
PyaazMani Core Grading Service Pipeline
Orchestrates AI feature extraction, grade classification, disease pathology, URS% & ledger hashing.
"""

from datetime import datetime
from backend.ai_grader import grade_onion
from backend.disease_detector import detect_disease_and_urs
from backend.database import get_last_hash, save_record
from backend.ledger import prepare_record


def calculate_quality_score(confidence: float, grade: str, features: list, disease_info: dict) -> float:
    """Calculate normalized quality index (0 - 100)."""
    score = confidence * 100.0

    if grade == "A":
        score += 8.0
    elif grade == "C":
        score -= 15.0

    # Spot ratio penalty
    spot_ratio = features[8] if len(features) > 8 else 0.0
    score -= min(35.0, spot_ratio * 150.0)

    # Circularity reward
    circularity = features[2] if len(features) > 2 else 0.8
    if circularity > 0.82:
        score += 4.0

    # Disease penalty
    if not disease_info.get("is_healthy", True):
        sev = disease_info.get("severity", "Low")
        if sev == "Severe":
            score -= 22.0
        elif sev == "Moderate":
            score -= 12.0
        else:
            score -= 6.0

    return round(max(5.0, min(99.5, score)), 1)


def estimate_price(grade: str, quality_score: float, disease_info: dict) -> float:
    """Indicative mandi valuation per 1 kg."""
    base_prices = {
        "A": 34.0,
        "B": 28.0,
        "C": 18.0
    }
    base = base_prices.get(grade, 25.0)

    # Fine adjustment based on quality score
    adjustment = (quality_score - 75.0) * 0.12
    price = base + adjustment

    if not disease_info.get("is_healthy", True) and disease_info.get("severity") == "Severe":
        price -= 4.5

    return round(max(10.0, price), 1)


def analyze_onion(
    image_path: str,
    farmer_name: str,
    farmer_id: str,
    lot_id: str,
    center: str,
    quantity: float,
    role: str = "farmer",
    lang: str = "en"
) -> dict:
    """
    Complete PyaazMani evaluation pipeline:
    Image -> ML Grader -> Disease Pathology -> URS% -> Price -> Cryptographic Ledger Record
    """
    # 1. AI Visual Grading
    ai_res = grade_onion(image_path)
    grade = ai_res["grade"]  # "A", "B", or "C"
    confidence = ai_res["confidence"]
    features = ai_res["features"]

    # 2. Disease Pathology & URS% Detection
    disease_info = detect_disease_and_urs(features=features, grade=grade, lang=lang)

    # 3. Quality Index & Pricing
    quality_score = calculate_quality_score(confidence, grade, features, disease_info)
    price_per_kg = estimate_price(grade, quality_score, disease_info)
    total_value = round(price_per_kg * quantity, 2)

    # 4. Prepare Ledger Entry
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    previous_hash = get_last_hash()

    record = {
        "farmer_name": farmer_name,
        "farmer_id": farmer_id,
        "lot_id": lot_id,
        "center": center,
        "quantity": quantity,
        "grade": grade,
        "confidence": confidence,
        "quality_score": quality_score,
        "urs_percentage": disease_info["urs_percentage"],
        "disease_name": disease_info["disease_name"],
        "disease_severity": disease_info["severity_text"],
        "remedy": disease_info["remedy"],
        "price_per_kg": price_per_kg,
        "total_value": total_value,
        "role": role,
        "timestamp": timestamp,
        "features": features
    }

    record = prepare_record(record, previous_hash)

    return {
        "grade": grade,
        "confidence": confidence,
        "quality_score": quality_score,
        "urs_percentage": disease_info["urs_percentage"],
        "disease_name": disease_info["disease_name"],
        "disease_severity": disease_info["severity_text"],
        "disease_severity_raw": disease_info["severity"],
        "remedy": disease_info["remedy"],
        "is_healthy": disease_info["is_healthy"],
        "price_per_kg": price_per_kg,
        "total_value": total_value,
        "features": features,
        "record": record
    }


def save_grading_result(result: dict) -> dict:
    """Persist grading record to SQLite."""
    record = result["record"]
    inserted_id = save_record(record)
    record["id"] = inserted_id
    return record