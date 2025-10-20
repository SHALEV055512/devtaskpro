from sqlalchemy import Column, String, Integer
from db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firstname = Column(String(100), nullable = False)
    lastname = Column(String(100), nullable = False)
    email = Column(String(100), unique=True, index=True ,nullable = False)
    password = Column(String(100), nullable = False)
    gender = Column(String(100), nullable = False)
    role = Column(String(100), nullable = False)
    team = Column(String(100), nullable = False)
