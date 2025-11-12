from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db import SessionLocal
import models
from security import hash_password, verify_password


# ============================================================
# CREATE USER
# ============================================================

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
        db.refresh(new_user)
        return new_user

    except Exception as e:
        db.rollback()
        print("❌ Error creating user:", e)
        raise

    finally:
        db.close()


# ============================================================
# GET USER BY EMAIL
# ============================================================

def get_user_by_email(email: str):
    email = email.lower().strip()
    db: Session = SessionLocal()
    try:
        return db.query(models.User).filter(models.User.email == email).first()
    finally:
        db.close()


# ============================================================
# AUTHENTICATE USER
# ============================================================

def authenticate_user(email: str, plain_password: str):
    email = email.lower().strip()
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.email == email).first()

        if not user:
            return {"success": False, "msg": "User does not exist"}

        if not verify_password(plain_password, user.password):
            return {"success": False, "msg": "Incorrect password"}

        return {"success": True, "role": user.role}

    finally:
        db.close()


# ============================================================
# UPDATE USER PASSWORD
# ============================================================

def update_user_password(email: str, new_password: str):
    email = email.lower().strip()
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            print(f"❌ No user found for {email}")
            return False

        user.password = hash_password(new_password)
        db.commit()
        db.refresh(user)
        print(f"✅ Password updated successfully for {email}")
        return True

    except Exception as e:
        db.rollback()
        print(f"❌ Error updating password for {email}: {e}")
        return False

    finally:
        db.close()

