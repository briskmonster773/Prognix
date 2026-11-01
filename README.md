
# Prognix
### AI-Powered Predictive Maintenance System

Prognix is a machine learning-based predictive maintenance web application that predicts potential machine failures using operational sensor data.

The system uses a trained XGBoost classification model to estimate failure probability and classify machine conditions as **Normal** or **Failure Risk**. It provides an interactive dashboard for manual machine assessment, simulated sensor monitoring, and prediction history management using SQLite.

## Features

- Machine failure prediction using a trained XGBoost model
- Failure probability estimation
- Manual machine assessment through an interactive dashboard
- Simulated machine sensor data generation
- Real-time simulator start and stop controls
- Machine condition classification: Normal or Failure Risk
- Prediction history stored in SQLite
- CSV logging of simulated predictions
- REST API built with FastAPI
- Interactive and responsive web dashboard

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
      Manual Input          Data Simulator
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
     Prediction Result       Data Storage
           |                       |
     Web Dashboard           SQLite / CSV
```

## Machine Parameters

The model uses six input features:

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

- **Failure Probability:** Estimated probability of machine failure
- **Decision Threshold:** Configured threshold used for classification
- **Prediction:** Binary classification (0 or 1)
- **Machine Status:** Normal or Failure Risk

> Note: Predictions are machine-learning estimates based on the training dataset. They do not guarantee actual machine safety or failure.

## Project Structure

```text
Prognix/
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
│
├── Dataset/
│
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/briskmonster773/Prognix.git
```

Navigate to the project directory:

```bash
cd Prognix
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the virtual environment.

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

### 4. Run the Application

From the project root:

```bash
python -m uvicorn backend.main:app --reload
```

### 5. Access the Application

| Service | URL |
|---|---|
| Web Dashboard | http://127.0.0.1:8000/ui/ |
| API Documentation | http://127.0.0.1:8000/docs |
| Health Check | http://127.0.0.1:8000/health |

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
- Automated maintenance scheduling and alerts
- Model performance monitoring
- Cloud deployment
- Role-based authentication

## Author

**Animish Kulkarni**

B.Tech – Artificial Intelligence & Analytics

- GitHub: https://github.com/briskmonster773
- LinkedIn: https://www.linkedin.com/in/animish-kulkarni-7b532a28a/

---

**Prognix — Predict Failures. Prevent Downtime. Optimize Performance.**
