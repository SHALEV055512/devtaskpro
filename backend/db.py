
import os
import models
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from db import SessionLocal
from typing import Optional



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'devtaskpro.db')}"
engine = create_engine(DATABASE_URL, echo = True)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_user_by_email(email: str):
    db: Session = SessionLocal()
    try:
        return db.query(models.User).filter(models.User.email == email).first()
    finally:
        db.close()

