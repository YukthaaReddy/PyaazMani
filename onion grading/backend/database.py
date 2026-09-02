"""
PyaazMani SQLite Database Manager
Provides persistent tamper-evident storage for onion lot quality certifications.
"""

import sqlite3
from pathlib import Path
from typing import List, Dict, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "onionsetu.db"


def get_connection():
    return sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False
    )


def initialize_database():
    """Create table if not exists and perform schema migration for new columns."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grading_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_name TEXT NOT NULL,
            farmer_id TEXT NOT NULL,
            lot_id TEXT NOT NULL,
            center TEXT NOT NULL,
            quantity REAL NOT NULL,
            grade TEXT NOT NULL,
            confidence REAL NOT NULL,
            quality_score REAL NOT NULL,
            urs_percentage REAL DEFAULT 0.0,
            disease_name TEXT DEFAULT 'Healthy',
            disease_severity TEXT DEFAULT 'None',
            price_per_kg REAL DEFAULT 25.0,
            total_value REAL DEFAULT 2500.0,
            role TEXT DEFAULT 'farmer',
            timestamp TEXT NOT NULL,
            previous_hash TEXT NOT NULL,
            record_hash TEXT NOT NULL
        )
    """)

    # Ensure backward compatibility by checking existing columns
    cursor.execute("PRAGMA table_info(grading_records)")
    columns = [col[1] for col in cursor.fetchall()]

    new_cols = [
        ("urs_percentage", "REAL DEFAULT 0.0"),
        ("disease_name", "TEXT DEFAULT 'Healthy'"),
        ("disease_severity", "TEXT DEFAULT 'None'"),
        ("price_per_kg", "REAL DEFAULT 25.0"),
        ("total_value", "REAL DEFAULT 2500.0"),
        ("role", "TEXT DEFAULT 'farmer'")
    ]

    for col_name, col_type in new_cols:
        if col_name not in columns:
            try:
                cursor.execute(f"ALTER TABLE grading_records ADD COLUMN {col_name} {col_type}")
            except Exception:
                pass

    connection.commit()
    connection.close()


def get_last_hash() -> str:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT record_hash
        FROM grading_records
        ORDER BY id DESC
        LIMIT 1
    """)
    result = cursor.fetchone()
    connection.close()
    if result:
        return result[0]
    return "0"


def save_record(record: dict) -> int:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO grading_records (
            farmer_name,
            farmer_id,
            lot_id,
            center,
            quantity,
            grade,
            confidence,
            quality_score,
            urs_percentage,
            disease_name,
            disease_severity,
            price_per_kg,
            total_value,
            role,
            timestamp,
            previous_hash,
            record_hash
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record.get("farmer_name", ""),
        record.get("farmer_id", ""),
        record.get("lot_id", ""),
        record.get("center", ""),
        float(record.get("quantity", 100.0)),
        record.get("grade", "A"),
        float(record.get("confidence", 0.9)),
        float(record.get("quality_score", 85.0)),
        float(record.get("urs_percentage", 2.0)),
        record.get("disease_name", "Healthy"),
        record.get("disease_severity", "None"),
        float(record.get("price_per_kg", 25.0)),
        float(record.get("total_value", 2500.0)),
        record.get("role", "farmer"),
        record.get("timestamp", ""),
        record.get("previous_hash", "0"),
        record.get("record_hash", "")
    ))

    inserted_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return inserted_id


def get_all_records() -> List[Dict]:
    """Return all grading records as formatted dictionary list."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            farmer_name,
            farmer_id,
            lot_id,
            center,
            quantity,
            grade,
            confidence,
            quality_score,
            urs_percentage,
            disease_name,
            disease_severity,
            price_per_kg,
            total_value,
            role,
            timestamp,
            previous_hash,
            record_hash
        FROM grading_records
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    connection.close()

    records = []
    for r in rows:
        records.append({
            "id": r[0],
            "farmer_name": r[1],
            "farmer_id": r[2],
            "lot_id": r[3],
            "center": r[4],
            "quantity": r[5],
            "grade": r[6],
            "confidence": r[7],
            "quality_score": r[8],
            "urs_percentage": r[9] if len(r) > 9 and r[9] is not None else 2.5,
            "disease_name": r[10] if len(r) > 10 and r[10] is not None else "Healthy",
            "disease_severity": r[11] if len(r) > 11 and r[11] is not None else "None",
            "price_per_kg": r[12] if len(r) > 12 and r[12] is not None else 25.0,
            "total_value": r[13] if len(r) > 13 and r[13] is not None else 2500.0,
            "role": r[14] if len(r) > 14 and r[14] is not None else "farmer",
            "timestamp": r[15],
            "previous_hash": r[16],
            "record_hash": r[17]
        })
    return records