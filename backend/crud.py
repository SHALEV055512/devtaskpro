from db import SessionLocal
from models import User

def create_user(data: dict):
    db = SessionLocal()
    new_user = User(
        email=data["email"],
        firstname=data["firstname"],
        lastname=data["lastname"],
        password=data["password"],
        gender=data["gender"],
        role=data["role"],
        team=data["team"]
    )
    db.add(new_user)
    db.commit()
    db.close()

    