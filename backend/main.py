import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel,Field
from typing import Literal
import pickle
from pathlib import Path
from backend.database import create_table, save_prediction, get_all_predictions
import subprocess
import sys
from fastapi.staticfiles import StaticFiles

app = FastAPI()

create_table()

MODEL_PATH = (
    Path(__file__).resolve().parent
    / "models"
    / "predictive_maintenance_xgb.pkl"
)

with open(MODEL_PATH, "rb") as model_file:
    model_bundle = pickle.load(model_file)

model_pipeline = model_bundle["pipeline"]
threshold = model_bundle["threshold"]

class MachineReading(BaseModel):
    machine_type: Literal["L", "M", "H"]
    air_temperature: float = Field(ge=0)
    process_temperature: float = Field(ge=0)
    rotational_speed: float = Field(gt=0)
    torque: float = Field(gt=0)
    tool_wear: float = Field(ge=0)


@app.post("/readings")
def receive_reading(reading: MachineReading):
    feature_mapping = {
        "Type": reading.machine_type,
        "Air temperature [K]": reading.air_temperature,
        "Process temperature [K]": reading.process_temperature,
        "Rotational speed [rpm]": reading.rotational_speed,
        "Torque [Nm]": reading.torque,
        "Tool wear [min]": reading.tool_wear
    }

    feature_cols = [
        "Type",
        "Air temperature [K]",
        "Process temperature [K]",
        "Rotational speed [rpm]",
        "Torque [Nm]",
        "Tool wear [min]"
    ]

    ordered_features = [
        feature_mapping[column] for column in feature_cols
    ]

    input_df = pd.DataFrame(
    [ordered_features],
    columns=feature_cols)

    probabilities = model_pipeline.predict_proba(input_df)
    failure_probability = float(probabilities[0][1])
    prediction = int(failure_probability >= threshold)

    return {
    "failure_probability": failure_probability,
    "threshold": threshold,
    "prediction": prediction,
    "status": "Failure Risk" if prediction == 1 else "Normal"}

@app.get("/")
def home():
    return {"message": "Predictive Maintenance API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}



@app.post("/manual/readings")
def receive_manual_reading(reading: MachineReading):
    feature_mapping = {
        "Type": reading.machine_type,
        "Air temperature [K]": reading.air_temperature,
        "Process temperature [K]": reading.process_temperature,
        "Rotational speed [rpm]": reading.rotational_speed,
        "Torque [Nm]": reading.torque,
        "Tool wear [min]": reading.tool_wear
    }

    feature_cols = [
        "Type",
        "Air temperature [K]",
        "Process temperature [K]",
        "Rotational speed [rpm]",
        "Torque [Nm]",
        "Tool wear [min]"
    ]

    input_df = pd.DataFrame(
        [[feature_mapping[column] for column in feature_cols]],
        columns=feature_cols
    )

    probabilities = model_pipeline.predict_proba(input_df)
    failure_probability = float(probabilities[0][1])
    prediction = int(failure_probability >= threshold)

    result = {
        "failure_probability": failure_probability,
        "threshold": threshold,
        "prediction": prediction,
        "status": "Failure Risk" if prediction == 1 else "Normal"
    }

    save_prediction(reading, result)

    return {
        **result,
        "message": "Manual prediction saved to database"
    }


@app.get("/manual/predictions")
def view_manual_predictions():
    predictions = get_all_predictions()

    return {
        "total_records": len(predictions),
        "predictions": predictions
    }



# Simulator process management
PROJECT_DIR = Path(__file__).resolve().parent.parent
SIMULATOR_PATH = PROJECT_DIR / "simulator" / "simulator.py"
FRONTEND_DIR = PROJECT_DIR / "frontend"

simulator_process = None


@app.post("/simulator/start")
def start_simulator():
    global simulator_process

    if simulator_process is not None and simulator_process.poll() is None:
        return {
            "status": "running",
            "message": "Simulator is already running"
        }

    if not SIMULATOR_PATH.exists():
        return {
            "status": "error",
            "message": f"Simulator not found: {SIMULATOR_PATH}"
        }

    try:
        simulator_process = subprocess.Popen(
            [sys.executable, "-u", str(SIMULATOR_PATH)],
            cwd=str(PROJECT_DIR),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        return {
            "status": "running",
            "message": "Simulator started"
        }

    except Exception as error:
        simulator_process = None
        return {
            "status": "error",
            "message": str(error)
        }


@app.post("/simulator/stop")
def stop_simulator():
    global simulator_process

    if simulator_process is not None and simulator_process.poll() is None:
        simulator_process.terminate()

        try:
            simulator_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            simulator_process.kill()
            simulator_process.wait()

    simulator_process = None

    return {
        "status": "stopped",
        "message": "Simulator stopped"
    }


@app.get("/simulator/status")
def simulator_status():
    running = (
        simulator_process is not None
        and simulator_process.poll() is None
    )

    return {
        "status": "running" if running else "stopped"
    }


# Serve frontend
app.mount(
    "/ui",
    StaticFiles(directory=str(FRONTEND_DIR), html=True),
    name="frontend"
)
