from backend.disease_detector import detect_disease_and_urs
from backend.service import calculate_quality_score, evaluate_lot


def test_grade_a_has_no_disease_and_low_urs():
    result = detect_disease_and_urs([1000, 90, 0.82, 20, 60, 120, 10, 2, 0.02, 0.02], "A", "en")
    assert result["is_healthy"] is True
    assert result["disease_name"] == "Healthy — No Pathological Infection"
    assert 0.0 <= result["urs_percentage"] <= 3.0


def test_grade_b_and_c_follow_grade_specific_urs_ranges():
    grade_b = detect_disease_and_urs([1000, 90, 0.82, 20, 60, 120, 10, 2, 0.02, 0.02], "B", "en")
    grade_c = detect_disease_and_urs([1000, 90, 0.82, 20, 60, 120, 10, 2, 0.08, 0.02], "C", "en")
    assert grade_b["urs_percentage"] > 5.0
    assert 5.0 <= grade_c["urs_percentage"] <= 8.0


def test_grade_score_ranges_are_enforced():
    assert 90 <= calculate_quality_score(0.95, "A", [0.8, 0.5, 0.82, 20, 60, 120, 10, 2, 0.02, 0.02], {"is_healthy": True}) <= 100
    assert 70 <= calculate_quality_score(0.85, "B", [0.8, 0.5, 0.82, 20, 60, 120, 10, 2, 0.04, 0.02], {"is_healthy": True}) <= 89
    assert 50 <= calculate_quality_score(0.75, "C", [0.8, 0.5, 0.82, 20, 60, 120, 10, 2, 0.08, 0.02], {"is_healthy": True}) <= 69


def test_severely_damaged_onion_is_rejected():
    result = evaluate_lot(
        grade="C",
        confidence=0.75,
        features=[0.8, 0.5, 0.82, 20, 60, 120, 10, 8, 0.18, 0.02],
        disease_info={"is_healthy": False, "severity": "Severe", "urs_percentage": 72, "disease_name": "Black Mould"},
    )

    assert result["rejected"] is True
    assert result["grade"] is None
    assert "cannot be consumed" in result["message"].lower()


def test_score_below_50_is_rejected_no_grade():
    result = evaluate_lot(
        grade="C",
        confidence=0.30,
        features=[0.8, 0.5, 0.82, 20, 60, 120, 10, 2, 0.08, 0.02],
        disease_info={"is_healthy": False, "severity": "Moderate", "urs_percentage": 25, "disease_name": "Purple Blotch"},
    )
    assert result["rejected"] is True
    assert result["grade"] is None
    assert result["quality_score"] < 50.0

