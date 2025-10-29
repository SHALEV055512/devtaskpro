from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi import HTTPException
import logging
from crud import create_user, get_user_by_email
from db import Base, engine
from schemas import UserCreate
from crud import authenticate_user 
import models

import json
app = FastAPI()


Base.metadata.create_all(bind=engine)

app.add_middleware(
     CORSMiddleware,
     allow_origins = ["*"],
     allow_credentials = True,
     allow_methods = ["*"],
     allow_headers =["*"]
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



@app.get("/help")
async def help():
    return {"status": "ok", "message": "Backend is alive!"}

   
@app.post("/api/register")
async def register(user: UserCreate):
    logger.info("📩 Registration request received")
    logger.info(f"Payload (without password): {user.model_dump(exclude={'password'})}")

    existing_user = get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email is already registered"
        )

    print(user.model_dump(exclude={'password'}))
    create_user(user.model_dump())
    return {"message": "User created"}  

@app.post("/auth/login")
async def login(request: Request):
    try:
        data = await request.json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            raise HTTPException(status_code=400, detail="Email and password are required")
        
        result = authenticate_user(email, password)

        if result == "user_not_found":
            raise HTTPException(status_code=404, detail="User does not exist")
        elif result == "wrong_password":
            raise HTTPException(status_code=401, detail="Incorrect password")
        
        return {"role": result}

    except Exception as e:
        logger.error(f"❌ Login failed: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
