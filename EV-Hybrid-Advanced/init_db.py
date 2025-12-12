from app.db import Base, engine
from app.models_orm import User, Prediction

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Done.")
