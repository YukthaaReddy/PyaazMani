"""
PyaazMani Disease Detection & URS% Assessment Engine
Analyzes visual features, color distributions, and surface necroses.
"""

from backend.i18n import t

def detect_disease_and_urs(features: list, grade: str, lang: str = "en") -> dict:
    """
    Analyzes visual features extracted from the onion image to determine:
    1. Disease / Defect status
    2. Severity (Low, Moderate, Severe, or None)
    3. URS % (Under-sized, Rot & Spot percentage)
    4. Actionable treatment advice in selected language
    
    Feature vector schema:
    [0]: area, [1]: perimeter, [2]: circularity, [3]: avg_hue,
    [4]: avg_sat, [5]: avg_bright, [6]: bright_std, [7]: spot_count,
    [8]: spot_ratio, [9]: edge_density
    """
    area = features[0]
    circularity = features[2]
    avg_hue = features[3]
    avg_sat = features[4]
    avg_bright = features[5]
    bright_std = features[6]
    spot_count = features[7]
    spot_ratio = features[8]
    edge_density = features[9]

    # ----------------------------------------------------
    # 1. CALCULATE URS % (Under-sized, Rot & Spot rate)
    # ----------------------------------------------------
    # Base baseline from Grade
    if grade == "A":
        base_urs = 0.0 + (spot_ratio * 12.0) + (max(0.0, 0.90 - circularity) * 2.0)
    elif grade == "B":
        base_urs = 6.0 + (spot_ratio * 30.0) + (max(0.0, 0.80 - circularity) * 6.0)
    else:  # Grade C
        base_urs = 6.0 + (spot_ratio * 24.0) + (max(0.0, 0.75 - circularity) * 10.0)

    urs_percentage = round(min(8.0, max(0.0, base_urs)), 1)
    if grade == "A" and urs_percentage < 0.1:
        urs_percentage = 0.0

    # ----------------------------------------------------
    # 2. PATHOLOGY / DISEASE CLASSIFICATION
    # ----------------------------------------------------
    disease_id = "disease_healthy"
    severity_id = "None"
    remedy_id = "remedy_healthy"

    if grade == "A" and spot_ratio <= 0.03 and spot_count <= 3:
        disease_id = "disease_healthy"
        severity_id = "None"
        remedy_id = "remedy_healthy"
    elif spot_ratio > 0.08 or (spot_count >= 8 and spot_ratio > 0.05):
        # High dark spotting with deep black clusters
        disease_id = "disease_black_mould"
        severity_id = "Severe" if spot_ratio > 0.12 else "Moderate"
        remedy_id = "remedy_black_mould"

    elif bright_std > 58.0 and spot_count >= 4:
        # Patchy purplish discoloration with sunken lesions
        disease_id = "disease_purple_blotch"
        severity_id = "Moderate" if spot_ratio > 0.04 else "Low"
        remedy_id = "remedy_purple_blotch"

    elif circularity < 0.55 and edge_density > 0.045:
        # Deformed contour with high edge irregularities (sprout protrusion or deep cuts)
        if avg_hue > 35 and avg_hue < 80:  # Greenish hue indicating sprout
            disease_id = "disease_sprouting"
            severity_id = "Moderate"
            remedy_id = "remedy_sprouting"
        else:
            disease_id = "disease_mechanical_damage"
            severity_id = "Moderate"
            remedy_id = "remedy_mechanical_damage"

    elif avg_bright < 110.0 and spot_ratio > 0.035 and circularity < 0.70:
        # Softening / water soaked neck rot
        disease_id = "disease_bacterial_soft_rot"
        severity_id = "Moderate" if spot_ratio > 0.06 else "Low"
        remedy_id = "remedy_bacterial_soft_rot"

    elif grade == "C" and spot_count > 3:
        disease_id = "disease_purple_blotch"
        severity_id = "Low"
        remedy_id = "remedy_purple_blotch"

    # Localized text outputs
    disease_name = t(disease_id, lang)
    disease_remedy = t(remedy_id, lang)

    # Severity localized tag
    severity_map = {
        "en": {"None": "None", "Low": "Low", "Moderate": "Moderate", "Severe": "High / Critical"},
        "hi": {"None": "शून्य", "Low": "हल्का (कम)", "Moderate": "मध्यम", "Severe": "गंभीर / अधिक"},
        "kn": {"None": "ಇಲ್ಲ", "Low": "ಕಡಿಮೆ", "Moderate": "ಮಧ್ಯಮ", "Severe": "ತೀವ್ರ / ಗಂಭೀರ"}
    }
    severity_text = severity_map.get(lang, severity_map["en"]).get(severity_id, severity_id)

    return {
        "disease_id": disease_id,
        "disease_name": disease_name,
        "severity": severity_id,
        "severity_text": severity_text,
        "remedy": disease_remedy,
        "urs_percentage": urs_percentage,
        "is_healthy": (disease_id == "disease_healthy")
    }
