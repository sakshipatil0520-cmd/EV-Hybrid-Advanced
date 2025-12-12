from app.db import SessionLocal
from app.models_orm import User
from app.auth import get_password_hash

db = SessionLocal()
existing = db.query(User).filter(User.username == "admin").first()

if existing:
    print("admin already exists")
else:
    u = User(
        username="admin",
        hashed_password=get_password_hash("adminpass"),
        full_name="Administrator",
        is_admin=True
    )
    db.add(u)
    db.commit()
    print("admin created")

db.close()
