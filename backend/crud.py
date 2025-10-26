from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db import SessionLocal
import models
from security import hash_password



def create_user(data: dict):
    db = SessionLocal()
    try: 
        new_user = models.User(
        email=data["email"],
        firstname=data["firstname"],
        lastname=data["lastname"],
        password=hash_password(data["password"]),
        gender=data["gender"],
        role=data["role"],
        team=data["team"]
    )
        db.add(new_user)
        db.commit()
    except Exception:
        db.rollback()   
        raise           
    finally:
        db.close()       

def get_user_by_email(email: str):
    import models 
    db: Session = SessionLocal()
    try:
        return db.query(models.User).filter(models.User.email == email).first()
    finally:
        db.close()
