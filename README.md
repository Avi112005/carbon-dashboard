# Carbon-Aware Scheduler

A lightweight tool that helps developers determine the **best time of day to run heavy computational tasks** by analyzing the **carbon intensity of the electricity grid**.

The project uses data from **Electricity Maps** and recommends execution windows that minimize carbon emissions.  
The grid zone can be changed easily to support different regions.

---

## What It Does

- Fetches carbon intensity time-series data for a selected grid zone
- Analyzes how carbon intensity varies over time
- Computes the optimal time window for a given task duration
- Compares **running now vs the best possible time**
- Reports **percentage carbon reduction**

---

## Example (IN-WE – Western India)

For a **2-hour task**:
- Run now: `590 gCO₂/kWh`
- Best time: `06:00`
- Carbon reduction: **~17.7%**

> The zone is configurable and can be changed to any supported Electricity Maps region.

---

## Tech Stack

- Python  
- Electricity Maps API (Sandbox)  
- `requests`, `python-dotenv`

---

## Setup

```bash
git clone https://github.com/<your-username>/carbon-aware-india
cd carbon-aware-india
pip install -r requirements.txt
```
Create a .env file:
```bash
ELECTRICITY_MAPS_API_KEY=your_api_key_here
```bash

Run:
```bash
python fetch_range.py
```