"""
PyaazMani Cryptographic Ledger Engine
Ensures tamper-evident SHA-256 digital seals for all grading decisions.
"""

import hashlib
import json


def create_record_hash(record: dict, previous_hash: str) -> str:
    data = {
        "farmer_name": str(record.get("farmer_name", "")),
        "farmer_id": str(record.get("farmer_id", "")),
        "lot_id": str(record.get("lot_id", "")),
        "center": str(record.get("center", "")),
        "quantity": float(record.get("quantity", 0.0)),
        "grade": str(record.get("grade", "A")),
        "confidence": float(record.get("confidence", 0.0)),
        "quality_score": float(record.get("quality_score", 0.0)),
        "urs_percentage": float(record.get("urs_percentage", 0.0)),
        "disease_name": str(record.get("disease_name", "")),
        "price_per_kg": float(record.get("price_per_kg", 0.0)),
        "timestamp": str(record.get("timestamp", "")),
        "previous_hash": str(previous_hash)
    }

    data_string = json.dumps(data, sort_keys=True)
    return hashlib.sha256(data_string.encode("utf-8")).hexdigest()


def prepare_record(record: dict, previous_hash: str) -> dict:
    record["previous_hash"] = previous_hash
    record["record_hash"] = create_record_hash(record, previous_hash)
    return record