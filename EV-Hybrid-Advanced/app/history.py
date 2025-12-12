import csv, os, json
from typing import List, Dict

LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "history.csv")

def append_history(timestamp: str, vin: str, input_dict: Dict, label: str, score: float):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, vin, json.dumps(input_dict), label, score])

def read_history_for_vin(vin: str):
    results = []
    if not os.path.exists(LOG_PATH):
        return results
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if r["vin"] == vin:
                try:
                    inp = json.loads(r["input"])
                except:
                    inp = {}
                results.append({"timestamp": r["timestamp"], "input": inp, "label": r["label"], "score": float(r["score"])})
    return results
