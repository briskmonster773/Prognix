
import random
import requests
import time
import csv
from pathlib import Path
from datetime import datetime

# FastAPI simulator endpoint
url = "http://127.0.0.1:8000/readings"

# CSV file location
CSV_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "simulator_predictions.csv"
)

# Create the data folder if it doesn't exist
CSV_PATH.parent.mkdir(parents=True, exist_ok=True)

# CSV column names
columns = [
    "timestamp",
    "machine_type",
    "air_temperature",
    "process_temperature",
    "rotational_speed",
    "torque",
    "tool_wear",
    "failure_probability",
    "threshold",
    "prediction",
    "status"
]

# Add the header only when the file is new or empty
if not CSV_PATH.exists() or CSV_PATH.stat().st_size == 0:
    with open(CSV_PATH, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()

while True:
    machine_reading = {
        "machine_type": random.choice(["L", "M", "H"]),
        "air_temperature": round(random.uniform(295, 305), 2),
        "process_temperature": round(random.uniform(305, 315), 2),
        "rotational_speed": random.randint(1200, 1800),
        "torque": round(random.uniform(30, 70), 2),
        "tool_wear": random.randint(0, 250)
    }

    print("\nSensor Reading:")
    print(machine_reading)

    try:
        response = requests.post(
            url,
            json=machine_reading,
            timeout=5
        )
        response.raise_for_status()

        result = response.json()

        # Combine sensor values and prediction
        csv_row = {
            "timestamp": datetime.now().isoformat(
                timespec="seconds"
            ),
            **machine_reading,
            "failure_probability": result["failure_probability"],
            "threshold": result["threshold"],
            "prediction": result["prediction"],
            "status": result["status"]
        }

        # Append one row to the CSV file
        with open(CSV_PATH, "a", newline="") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=columns
            )
            writer.writerow(csv_row)

        print(
            "Failure Probability:",
            round(result["failure_probability"] * 100, 2),
            "%"
        )
        print("Status:", result["status"])
        print("Saved to:", CSV_PATH)

    except requests.exceptions.RequestException as error:
        print("Backend connection error:", error)

    except (KeyError, ValueError) as error:
        print("Invalid prediction response:", error)

    print("Next reading in 5 seconds...")
    time.sleep(5)
