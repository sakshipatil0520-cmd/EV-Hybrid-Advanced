from fastapi import FastAPI
from .db import engine, Base
from .models_orm import User, Prediction 
from .router import router

app = FastAPI(title="EV Hybrid Advanced API")

app.include_router(router)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
