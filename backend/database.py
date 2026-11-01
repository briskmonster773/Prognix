
import sqlite3
from pathlib import Path

# Store the database in the project root folder
DATABASE_PATH = (
    Path(__file__).resolve().parent.parent
    / "maintenance.db"
)


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS manual_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_type TEXT NOT NULL,
            air_temperature REAL NOT NULL,
            process_temperature REAL NOT NULL,
            rotational_speed REAL NOT NULL,
            torque REAL NOT NULL,
            tool_wear INTEGER NOT NULL,
            failure_probability REAL NOT NULL,
            threshold REAL NOT NULL,
            prediction INTEGER NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_prediction(reading, result):
    connection = get_connection()

    connection.execute("""
        INSERT INTO manual_predictions (
            machine_type,
            air_temperature,
            process_temperature,
            rotational_speed,
            torque,
            tool_wear,
            failure_probability,
            threshold,
            prediction,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        reading.machine_type,
        reading.air_temperature,
        reading.process_temperature,
        reading.rotational_speed,
        reading.torque,
        reading.tool_wear,
        result["failure_probability"],
        result["threshold"],
        result["prediction"],
        result["status"]
    ))

    connection.commit()
    connection.close()

    
def get_all_predictions():
    connection = get_connection()

    rows = connection.execute("""
        SELECT * FROM manual_predictions
        ORDER BY id DESC
    """).fetchall()

    connection.close()

    return [dict(row) for row in rows]

