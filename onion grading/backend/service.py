"""
PyaazMani Core Grading Service Pipeline
Orchestrates AI feature extraction, grade classification, disease pathology, URS% & ledger hashing.
"""

from datetime import datetime
from backend.ai_grader import grade_onion
from backend.disease_detector import detect_disease_and_urs
from backend.database import get_last_hash, save_record
from backend.ledger import prepare_record


def evaluate_lot(grade: str | None, confidence: float, features: list, disease_info: dict) -> dict:
    """Reject lots that are unsafe or unsellable and enforce grade score ranges (Grade A: 90-100, Grade B: 70-89, Grade C: 50-69, Below 50: Rejected)."""
    severity = disease_info.get("severity", "Low")
    urs_percentage = float(disease_info.get("urs_percentage", 0.0) or 0.0)
    is_healthy = bool(disease_info.get("is_healthy", True))
    spot_ratio = features[8] if len(features) > 8 else 0.0

    score = confidence * 100.0
    if grade == "A":
        score += 8.0
    elif grade == "B":
        score -= 4.0
    elif grade == "C":
        score -= 10.0

    if not is_healthy:
        if severity == "Severe":
            score -= 30.0
        elif severity == "Moderate":
            score -= 15.0
        elif severity == "Low":
            score -= 5.0

    score -= (urs_percentage * 0.3)

    rejected = (
        (not is_healthy and severity == "Severe")
        or urs_percentage >= 50
        or spot_ratio >= 0.18
        or score < 50.0
    )

    if rejected:
        final_score = round(max(0.0, min(49.9, score)), 1)
        return {
            "rejected": True,
            "grade": None,
            "quality_score": final_score,
            "message": "This onion cannot be consumed. Its quality score is below 50 (or severely damaged), so it is qualified as REJECTED in red highlight and cannot be assigned any grade.",
        }

    score_ranges = {
        "A": (90.0, 100.0),
        "B": (70.0, 89.0),
        "C": (50.0, 69.0),
    }
    lower, upper = score_ranges.get(grade or "C", (50.0, 69.0))
    score = max(lower, min(upper, round(score, 1)))
    if grade == "A":
        score = max(90.0, min(100.0, score))
    elif grade == "B":
        score = max(70.0, min(89.0, score))
    elif grade == "C":
        score = max(50.0, min(69.0, score))

    return {
        "rejected": False,
        "grade": grade,
        "quality_score": round(score, 1),
        "message": "",
    }


def calculate_quality_score(confidence: float, grade: str, features: list, disease_info: dict) -> float:
    """Calculate normalized quality index in the required grade band."""
    return evaluate_lot(grade, confidence, features, disease_info)["quality_score"]


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
    ai_res = grade_onion(image_path)
    grade = ai_res["grade"]
    confidence = ai_res["confidence"]
    features = ai_res["features"]
    disease_info = detect_disease_and_urs(features=features, grade=grade, lang=lang)

    decision = evaluate_lot(grade, confidence, features, disease_info)
    if decision["rejected"]:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        previous_hash = get_last_hash()
        rejected_record = {
            "farmer_name": farmer_name,
            "farmer_id": farmer_id,
            "lot_id": lot_id,
            "center": center,
            "quantity": quantity,
            "grade": "REJECTED",
            "confidence": confidence,
            "quality_score": decision["quality_score"],
            "urs_percentage": disease_info["urs_percentage"],
            "disease_name": disease_info["disease_name"],
            "disease_severity": disease_info["severity_text"],
            "remedy": disease_info["remedy"],
            "price_per_kg": 0.0,
            "total_value": 0.0,
            "role": role,
            "timestamp": timestamp,
            "features": features
        }
        rejected_record = prepare_record(rejected_record, previous_hash)
        return {
            "grade": None,
            "confidence": confidence,
            "quality_score": decision["quality_score"],
            "urs_percentage": disease_info["urs_percentage"],
            "disease_name": disease_info["disease_name"],
            "disease_severity": disease_info["severity_text"],
            "disease_severity_raw": disease_info["severity"],
            "remedy": disease_info["remedy"],
            "is_healthy": disease_info["is_healthy"],
            "price_per_kg": 0.0,
            "total_value": 0.0,
            "features": features,
            "rejected": True,
            "message": decision["message"],
            "record": rejected_record,
        }

    quality_score = decision["quality_score"]
    price_per_kg = estimate_price(grade, quality_score, disease_info)
    total_value = round(price_per_kg * quantity, 2)

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
        "rejected": False,
        "message": "",
        "record": record
    }


def save_grading_result(result: dict) -> dict:
    """Persist grading record to SQLite."""
    record = result["record"]
    inserted_id = save_record(record)
    record["id"] = inserted_id
    return record