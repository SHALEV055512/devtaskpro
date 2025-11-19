from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

# --- DB & MODELS ---
from db import Base, engine
import models

# --- CRUD ---
from crud import create_user, get_user_by_email, authenticate_user

# --- SCHEMAS ---
from schemas import UserCreate
from pydantic import BaseModel, EmailStr

# --- EMAIL VERIFICATION ---
from mail.verify_email import send_auth_email
from mail.email_verification_manager import verify_token

# --- FORGOT PASSWORD FLOW ---
from mail.forgot_password import (
    request_password_reset,
    verify_reset_token,
    reset_password
)

# =====================================
# APP INITIALIZATION
# =====================================

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =====================================
# HEALTH CHECK
# =====================================

@app.get("/help")
async def help():
    return {"status": "ok", "message": "Backend is alive!"}


# =====================================
# REGISTER
# =====================================

@app.post("/api/register")
async def register(user: UserCreate):
    logger.info("📩 Registration request received")
    logger.info(f"Payload (excluding password): {user.model_dump(exclude={'password'})}")

    existing_user = get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already registered")

    send_auth_email(user.email, user.model_dump())
    return {"message": "Verification email sent successfully."}


# =====================================
# VERIFY EMAIL
# =====================================

class VerifyEmailRequest(BaseModel):
    email: EmailStr
    token: str


@app.post("/api/verify_email")
async def verify_email(data: VerifyEmailRequest):
    ok, result = verify_token(data.email, data.token)
    if not ok:
        raise HTTPException(status_code=400, detail=result)

    create_user(result)
    return {"message": "Email verified and user created successfully!"}


# =====================================
# LOGIN
# =====================================

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


# =====================================
# FORGOT PASSWORD
# =====================================

class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class VerifyResetCode(BaseModel):
    email: EmailStr
    token: str


class ResetPasswordRequest(BaseModel):
    password: str


@app.post("/api/forgot_password")
async def forgot_password(req: ForgotPasswordRequest):
    result = request_password_reset(req.email)

    # If failed → raise proper HTTPException with correct status
    if not result["success"]:
        raise HTTPException(
            status_code=result["status"],
            detail=result["message"]
        )

    # If success → respond normally
    return {"message": result["message"]}

@app.post("/api/verify_reset_token")
async def verify_reset(req: VerifyResetCode):
    result = verify_reset_token(req.email, req.token)

    if not result["success"]:
        raise HTTPException(
            status_code=result["status"],
            detail=result["message"]
        )

    return {"message": result["message"]}



@app.post("/api/reset_password")
async def reset_pw(req: ResetPasswordRequest):
    result = reset_password(req.password)

    if not result["success"]:
        raise HTTPException(
            status_code=result["status"],
            detail=result["message"]
        )

    return {"message": result["message"]}
