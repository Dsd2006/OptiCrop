
import sqlite3
from pathlib import Path
from datetime import datetime

DATABASE = Path(__file__).with_name("opticrop.db")


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nitrogen REAL NOT NULL,
            phosphorus REAL NOT NULL,
            potassium REAL NOT NULL,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL,
            ph REAL NOT NULL,
            rainfall REAL NOT NULL,
            recommended_crop TEXT NOT NULL,
            confidence REAL NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()

    print("OptiCrop database initialized successfully!")


def save_prediction(data, crop, confidence):
    connection = get_connection()

    connection.execute("""
        INSERT INTO predictions (
            nitrogen, phosphorus, potassium,
            temperature, humidity, ph, rainfall,
            recommended_crop, confidence, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        float(data["nitrogen"]),
        float(data["phosphorus"]),
        float(data["potassium"]),
        float(data["temperature"]),
        float(data["humidity"]),
        float(data["ph"]),
        float(data["rainfall"]),
        crop,
        float(confidence),
        datetime.now().strftime("%d-%m-%Y %I:%M %p")
    ))

    connection.commit()
    connection.close()


def get_prediction_history(limit=10):
    connection = get_connection()

    history = connection.execute("""
        SELECT *
        FROM predictions
        ORDER BY id DESC
        LIMIT ?
    """, (limit,)).fetchall()

    connection.close()

    return [dict(row) for row in history]


def get_dashboard_stats():
    connection = get_connection()

    total = connection.execute("""
        SELECT COUNT(*) FROM predictions
    """).fetchone()[0]

    different_crops = connection.execute("""
        SELECT COUNT(DISTINCT recommended_crop)
        FROM predictions
    """).fetchone()[0]

    latest = connection.execute("""
        SELECT *
        FROM predictions
        ORDER BY id DESC
        LIMIT 1
    """).fetchone()

    connection.close()

    return {
        "total_predictions": total,
        "different_crops": different_crops,
        "latest_prediction": dict(latest) if latest else None
    }
