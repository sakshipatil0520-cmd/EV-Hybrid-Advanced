
def predict_fault(features: dict):
   
    battery = float(features.get("battery_level", 50))
    motor_temp = float(features.get("motor_temp", 60))
    mileage = float(features.get("mileage", 10000))
    cycles = int(features.get("charging_cycles", 100))

    score = 0.0
    if battery < 20:
        score += 0.5
    if motor_temp > 90:
        score += 0.6
    if cycles > 1000:
        score += 0.2
    if mileage > 200000:
        score += 0.2

    if score > 1.0:
        score = 1.0

    label = "Fault" if score >= 0.5 else "OK"
    return label, round(float(score), 2)
