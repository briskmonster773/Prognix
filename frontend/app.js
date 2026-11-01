
const API = "";

const $ = (id) => document.getElementById(id);


// Send requests to the FastAPI backend
async function apiRequest(path, options = {}) {
    const response = await fetch(API + path, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...options.headers
        }
    });

    if (!response.ok) {
        const detail = await response.text();
        throw new Error(detail || `Request failed: ${response.status}`);
    }

    return response.json();
}


// Display success and error messages
function showMessage(id, message, isError = false) {
    const element = $(id);

    if (!element) return;

    element.textContent = message;
    element.classList.toggle("error", isError);
}


// Update simulator status on the dashboard
function setSimulatorStatus(status) {
    const running = status === "running";
    const pill = $("simStatus");

    pill.textContent = running
        ? "● Simulator running"
        : "● Simulator stopped";

    pill.className =
        "status-pill " + (running ? "running" : "stopped");

    $("startBtn").disabled = running;
    $("stopBtn").disabled = !running;
}


// Get the current simulator status
async function refreshSimulatorStatus() {
    try {
        const result = await apiRequest("/simulator/status");

        setSimulatorStatus(result.status);

    } catch (error) {
        $("simStatus").textContent = "API unavailable";
        $("simStatus").className = "status-pill error";

        $("startBtn").disabled = true;
        $("stopBtn").disabled = true;
    }
}


// Start the simulator
$("startBtn").addEventListener("click", async () => {
    $("startBtn").disabled = true;

    showMessage("simMessage", "Starting simulator...");

    try {
        const result = await apiRequest("/simulator/start", {
            method: "POST"
        });

        if (result.status === "error") {
            throw new Error(result.message || "Could not start simulator.");
        }

        setSimulatorStatus(result.status);

        showMessage("simMessage", result.message);

    } catch (error) {
        showMessage("simMessage", error.message, true);

        await refreshSimulatorStatus();
    }
});


// Stop the simulator
$("stopBtn").addEventListener("click", async () => {
    $("stopBtn").disabled = true;

    showMessage("simMessage", "Stopping simulator...");

    try {
        const result = await apiRequest("/simulator/stop", {
            method: "POST"
        });

        setSimulatorStatus(result.status);

        showMessage("simMessage", result.message);

    } catch (error) {
        showMessage("simMessage", error.message, true);

        await refreshSimulatorStatus();
    }
});


// Submit a manual machine reading for prediction
$("predictionForm").addEventListener("submit", async (event) => {
    event.preventDefault();

    const reading = {
        machine_type: $("machine_type").value,
        air_temperature: Number($("air_temperature").value),
        process_temperature: Number($("process_temperature").value),
        rotational_speed: Number($("rotational_speed").value),
        torque: Number($("torque").value),
        tool_wear: Number($("tool_wear").value)
    };

    $("predictBtn").disabled = true;
    $("predictBtn").textContent = "Analyzing...";

    showMessage("formMessage", "");

    try {
        const result = await apiRequest("/manual/readings", {
            method: "POST",
            body: JSON.stringify(reading)
        });

        const percent = result.failure_probability * 100;
        const risk = Number(result.prediction) === 1;

        // Display the prediction result
        $("resultCard").classList.remove(
            "hidden",
            "risk",
            "normal"
        );

        $("resultCard").classList.add(
            risk ? "risk" : "normal"
        );

        $("resultStatus").textContent = result.status;

        $("resultDescription").textContent = risk
            ? "The model estimates elevated failure risk. Inspect the machine and follow appropriate maintenance procedures."
            : "The estimated probability is below the configured decision threshold.";

        $("resultProbability").textContent =
            percent.toFixed(2) + "%";

        $("probabilityBar").style.width =
            Math.min(100, Math.max(0, percent)) + "%";

        $("thresholdText").textContent =
            "Decision threshold: " +
            (result.threshold * 100).toFixed(0) + "%";

        // Update the latest prediction metrics
        $("latestProbability").textContent =
            percent.toFixed(2) + "%";

        $("latestStatus").textContent = result.status;

        showMessage(
            "formMessage",
            result.message || "Prediction saved to SQLite successfully."
        );

        // Refresh the history after saving the prediction
        await loadHistory();

    } catch (error) {
        showMessage(
            "formMessage",
            "Could not generate prediction: " + error.message,
            true
        );

    } finally {
        $("predictBtn").disabled = false;
        $("predictBtn").textContent = "Analyze Machine →";
    }
});


// Load saved manual predictions from the backend
async function loadHistory() {
    const body = $("historyBody");

    try {
        showMessage(
            "historyMessage",
            "Loading prediction history..."
        );

        const result = await apiRequest("/manual/predictions");
        const records = result.predictions || [];

        $("recordCount").textContent =
            result.total_records ?? records.length;

        // Clear old table rows before rendering new records
        body.replaceChildren();

        if (records.length === 0) {
            const row = document.createElement("tr");
            const cell = document.createElement("td");

            cell.colSpan = 8;
            cell.className = "empty-state";
            cell.textContent = "No manual predictions saved yet.";

            row.appendChild(cell);
            body.appendChild(row);

            showMessage(
                "historyMessage",
                "No saved predictions found."
            );

            return;
        }

        // Create one row for each saved prediction
        records.forEach((record) => {
            const row = document.createElement("tr");

            const values = [
                `${record.id} · ${record.created_at || ""}`,
                record.machine_type,
                `${Number(record.air_temperature).toFixed(2)} / ${Number(record.process_temperature).toFixed(2)}`,
                Number(record.rotational_speed).toFixed(0),
                Number(record.torque).toFixed(2),
                record.tool_wear,
                `${(Number(record.failure_probability) * 100).toFixed(2)}%`
            ];

            values.forEach((value) => {
                const cell = document.createElement("td");

                cell.textContent = value ?? "";

                row.appendChild(cell);
            });

            // Add the prediction status
            const statusCell = document.createElement("td");
            const badge = document.createElement("span");

            badge.className =
                "status-text " +
                (Number(record.prediction) === 1
                    ? "risk"
                    : "normal");

            badge.textContent = record.status;

            statusCell.appendChild(badge);
            row.appendChild(statusCell);

            body.appendChild(row);
        });

        showMessage(
            "historyMessage",
            `Loaded ${records.length} manual prediction(s).`
        );

    } catch (error) {
        console.error("History loading error:", error);

        showMessage(
            "historyMessage",
            "Could not load history: " + error.message,
            true
        );
    }
}


// Refresh the prediction history when the button is clicked
$("refreshBtn").addEventListener("click", async () => {
    const button = $("refreshBtn");

    button.disabled = true;
    button.textContent = "Refreshing...";

    try {
        await loadHistory();

    } finally {
        button.disabled = false;
        button.textContent = "↻ Refresh";
    }
});


// Initial dashboard setup
refreshSimulatorStatus();
loadHistory();


// Check simulator status every 3 seconds
setInterval(refreshSimulatorStatus, 3000);
