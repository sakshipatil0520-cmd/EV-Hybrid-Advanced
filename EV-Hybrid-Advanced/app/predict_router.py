from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import csv, os, json, datetime

from .db import get_db
from .schemas import PredictionRequest, PredictionResponse
from .ml.predict import predict_fault

router = APIRouter()

LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "history.csv")
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
if not os.path.exists(LOG_PATH):
    with open(LOG_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "vin", "input", "label", "score"])


@router.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest, db: Session = Depends(get_db)):
    label, score = predict_fault({
        "battery_level": payload.battery_level,
        "motor_temp": payload.motor_temp,
        "mileage": payload.mileage,
        "charging_cycles": payload.charging_cycles
    })

    timestamp = datetime.datetime.utcnow().isoformat()
    with open(LOG_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, payload.vin or "", json.dumps(payload.dict()), label, score])

    return {"label": label, "score": score}


@router.get("/vehicle/latest/{vin}")
def vehicle_latest(vin: str):
    rows = []
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if r["vin"] == vin:
                rows.append(r)
    if not rows:
        raise HTTPException(status_code=404, detail="No data for VIN")
    last = rows[-1]
    try:
        input_json = json.loads(last["input"])
    except Exception:
        input_json = {}
    return {
        "vin": vin,
        "input": input_json,
        "label": last["label"],
        "score": float(last["score"]),
        "timestamp": last["timestamp"]
    }


@router.get("/vehicle/history/{vin}")
def vehicle_history(vin: str):
    records = []
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if r["vin"] == vin:
                try:
                    r_input = json.loads(r["input"])
                except Exception:
                    r_input = {}
                records.append({
                    "timestamp": r["timestamp"],
                    "vin": r["vin"],
                    "input": r_input,
                    "label": r["label"],
                    "score": float(r["score"])
                })
    return records
