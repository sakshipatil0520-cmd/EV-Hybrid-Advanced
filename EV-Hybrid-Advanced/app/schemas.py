from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginForm(BaseModel):
    username: str
    password: str

class CreateAdminForm(BaseModel):
    username: str
    password: str
    full_name: Optional[str] = "Admin"

class PredictionRequest(BaseModel):
    vin: Optional[str] = None
    battery_level: float
    motor_temp: float
    mileage: float
    charging_cycles: int

class PredictionResponse(BaseModel):
    label: str
    score: float
