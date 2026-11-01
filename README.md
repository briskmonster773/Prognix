
# MaintenIQ – AI-Powered Predictive Maintenance System

MaintenIQ is a machine learning-based predictive maintenance web application that predicts potential machine failures using operational sensor data.

The system uses a trained XGBoost classification model to estimate failure probability and classify machine conditions as Normal or Failure Risk. It provides a web dashboard for manual machine assessment, simulated sensor monitoring, and prediction history management using SQLite.

## Features

- **Machine Failure Prediction:** Predicts potential machine failures using a trained XGBoost model.
- **Failure Probability Estimation:** Displays the estimated probability of machine failure.
- **Manual Machine Assessment:** Allows users to enter machine parameters and generate predictions.
- **Sensor Data Simulation:** Generates simulated machine readings for continuous monitoring.
- **Interactive Dashboard:** Displays prediction results, machine status, and simulator controls.
- **Prediction History:** Stores manual predictions in an SQLite database.
- **REST API:** Provides API endpoints using FastAPI.
- **Data Logging:** Stores simulated predictions in CSV format.

## Tech Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Machine Learning | XGBoost, Scikit-learn |
| Data Processing | Pandas, NumPy |
| Backend | FastAPI |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite |
| API Server | Uvicorn |
| Dataset | AI4I 2020 Predictive Maintenance Dataset |

## System Architecture

```text
             Machine Sensor Data
                      |
          +-----------+-----------+
          |                       |
    Manual Input            Data Simulator
          |                       |
          +-----------+-----------+
                      |
                FastAPI Backend
                      |
            Data Preprocessing
                      |
          Trained XGBoost Model
                      |
          Failure Probability
                      |
          +-----------+-----------+
          |                       |
     Prediction Result      Data Storage
          |                       |
    Web Dashboard          SQLite / CSV
```

## Machine Parameters

The model uses the following six input features:

| Parameter | Description |
|---|---|
| Machine Type | Machine quality type: L, M, or H |
| Air Temperature (K) | Ambient air temperature |
| Process Temperature (K) | Machine process temperature |
| Rotational Speed (RPM) | Machine rotational speed |
| Torque (Nm) | Torque applied to the machine |
| Tool Wear (min) | Accumulated tool wear time |

## Prediction Output

The system provides:

- Failure Probability: Estimated probability of machine failure.
- Decision Threshold: Configured threshold used for classification.
- Prediction: Binary classification (0 or 1).
- Machine Status:
  - Normal
  - Failure Risk

**Note:** Predictions are machine-learning estimates based on the training dataset. They do not guarantee actual machine safety or failure.

## Project Structure

```text
Prective Maintaince/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── requirements.txt
│   └── models/
│       └── predictive_maintenance_xgb.pkl
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── simulator/
│   └── simulator.py
│
├── data/
│   └── simulator_predictions.csv
│
├── Dataset/
│
├── maintenance.db
│
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/MaintenIQ.git
```

Navigate to the project directory:

```bash
cd Prognix
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment.

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```cmd
.venv\Scripts\activate.bat
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Run the FastAPI Backend

From the project root:

```bash
python -m uvicorn backend.main:app --reload
```

### 5. Open the Application

Dashboard:

http://127.0.0.1:8000/ui/

API documentation (Swagger):

http://127.0.0.1:8000/docs

Health check:

http://127.0.0.1:8000/health

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API welcome message |
| GET | `/health` | Check API health |
| POST | `/readings` | Process simulated machine readings |
| POST | `/manual/readings` | Generate and save a manual prediction |
| GET | `/manual/predictions` | Retrieve saved prediction history |
| POST | `/simulator/start` | Start the data simulator |
| POST | `/simulator/stop` | Stop the data simulator |
| GET | `/simulator/status` | Check simulator status |

## Dataset

This project uses the **AI4I 2020 Predictive Maintenance Dataset**, which contains synthetic industrial machine data designed for predictive maintenance research.

Dataset source:

https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset

## Future Enhancements

- Real-time IoT sensor integration
- Live machine health monitoring
- Advanced analytics and visualization
- Maintenance scheduling and alerts
- Model performance monitoring
- Cloud deployment
- Role-based authentication

## Author

**Animish Kulkarni**

B.Tech – Artificial Intelligence & Analytics

GitHub: https://github.com/YOUR_USERNAME

LinkedIn: https://www.linkedin.com/in/animish-kulkarni-7b532a28a/

---

Prognix – Predict Failures. Prevent Downtime. Optimize Performance.*
