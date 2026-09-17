import pytest
from backend.service import analyze_onion, evaluate_lot, calculate_quality_score, estimate_price
from backend.pdf_generator import generate_pdf_report
from backend.auth import get_role_info, ROLES
from backend.i18n import t, TRANSLATIONS


def test_grade_a_score_range():
    res = evaluate_lot("A", 0.95, [0.8, 0.5, 0.82, 20, 60, 120, 10, 2, 0.02, 0.02], {"is_healthy": True})
    assert res["rejected"] is False
    assert res["grade"] == "A"
    assert 90.0 <= res["quality_score"] <= 100.0


def test_grade_b_score_range():
    res = evaluate_lot("B", 0.85, [0.8, 0.5, 0.82, 20, 60, 120, 10, 2, 0.04, 0.02], {"is_healthy": True})
    assert res["rejected"] is False
    assert res["grade"] == "B"
    assert 70.0 <= res["quality_score"] <= 89.0


def test_grade_c_score_range():
    res = evaluate_lot("C", 0.75, [0.8, 0.5, 0.82, 20, 60, 120, 10, 2, 0.08, 0.02], {"is_healthy": True})
    assert res["rejected"] is False
    assert res["grade"] == "C"
    assert 50.0 <= res["quality_score"] <= 69.0


def test_below_50_rejected():
    res = evaluate_lot("C", 0.20, [0.8, 0.5, 0.82, 20, 60, 120, 10, 2, 0.08, 0.02], {"is_healthy": False, "severity": "Moderate", "urs_percentage": 30.0})
    assert res["rejected"] is True
    assert res["grade"] is None
    assert res["quality_score"] < 50.0


def test_pdf_generation_graded_and_rejected():
    record_graded = {
        "id": 1,
        "farmer_name": "Ramesh",
        "farmer_id": "F100",
        "lot_id": "LOT-100",
        "center": "Nashik",
        "quantity": 100.0,
        "grade": "A",
        "confidence": 0.95,
        "quality_score": 95.0,
        "urs_percentage": 2.0,
        "disease_name": "Healthy",
        "disease_severity": "None",
        "price_per_kg": 35.0,
        "total_value": 3500.0,
        "role": "official",
        "timestamp": "2026-09-17 10:00:00",
        "record_hash": "abcdef1234567890"
    }
    pdf_graded = generate_pdf_report(record_graded)
    assert isinstance(pdf_graded, bytes)
    assert len(pdf_graded) > 1000

    record_rejected = {
        "id": 2,
        "farmer_name": "Suresh",
        "farmer_id": "F101",
        "lot_id": "LOT-101",
        "center": "Nashik",
        "quantity": 50.0,
        "grade": "REJECTED",
        "confidence": 0.40,
        "quality_score": 42.0,
        "urs_percentage": 60.0,
        "disease_name": "Black Mould",
        "disease_severity": "Severe",
        "price_per_kg": 0.0,
        "total_value": 0.0,
        "role": "official",
        "timestamp": "2026-09-17 10:05:00",
        "record_hash": "1234567890abcdef"
    }
    pdf_rejected = generate_pdf_report(record_rejected)
    assert isinstance(pdf_rejected, bytes)
    assert len(pdf_rejected) > 1000


def test_government_official_role_has_reports_chapter():
    info = get_role_info("official")
    assert "reports" in info["allowed_fragments"]
    assert t("nav_reports", "en") == "Official PDF Report and History"
