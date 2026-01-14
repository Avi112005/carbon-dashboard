import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
API_KEY = os.getenv("ELECTRICITY_MAPS_API_KEY")
ZONE = "IN" #change this to test different zones
TASK_DURATION_HOURS = 2  # change this to test different durations

if not API_KEY:
    raise RuntimeError(
        "Missing ELECTRICITY_MAPS_API_KEY. "
        "Set it in a .env file or environment variable."
    )

# Electricity Maps API endpoint
URL = "https://api.electricitymaps.com/v3/carbon-intensity/past-range"

PARAMS = {
    "zone": ZONE,
    "start": "2026-01-13T00:00:00Z",
    "end": "2026-01-14T23:59:00Z"
}

HEADERS = {
    "auth-token": API_KEY
}

# Fetch carbon intensity data
response = requests.get(URL, params=PARAMS, headers=HEADERS)
response.raise_for_status()

data = response.json().get("data", [])

if not data:
    raise RuntimeError("No carbon intensity data received from API")

# Convert API data to (datetime, carbonIntensity)
points = []
for item in data:
    timestamp = datetime.fromisoformat(item["datetime"].replace("Z", ""))
    intensity = item["carbonIntensity"]
    points.append((timestamp, intensity))

# Carbon-aware optimization logic
best_avg = float("inf")
best_start = None

for i in range(len(points)):
    window = points[i:i + TASK_DURATION_HOURS]

    if len(window) < TASK_DURATION_HOURS:
        break

    avg_intensity = sum(p[1] for p in window) / TASK_DURATION_HOURS

    if avg_intensity < best_avg:
        best_avg = avg_intensity
        best_start = window[0][0]

# Baseline: run immediately
now_window = points[:TASK_DURATION_HOURS]
now_avg = sum(p[1] for p in now_window) / TASK_DURATION_HOURS

# Results
print("\n=== CARBON-AWARE SCHEDULER RESULT ===")
print(f"Zone: {ZONE}")
print(f"Task duration: {TASK_DURATION_HOURS} hours")
print(f"Run now avg carbon: {now_avg:.1f} gCO₂/kWh")
print(f"Best start time: {best_start}")
print(f"Best avg carbon: {best_avg:.1f} gCO₂/kWh")
print(
    f"Carbon reduction: {((now_avg - best_avg) / now_avg) * 100:.1f}%"
)