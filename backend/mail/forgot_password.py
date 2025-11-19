# =============================================================
# PASSWORD RESET MANAGER — REDIS VERSION (FIXED)
# =============================================================

import time
import json
import redis
from crud import get_user_by_email, update_user_password
from schemas import PasswordReset
from mail.verify_email import send_auth_email

# =============================================================
# CONNECT TO REDIS
# =============================================================

r = redis.StrictRedis(
    host="redis",
    port=6379,
    decode_responses=True
)


# =============================================================
# 1) REQUEST PASSWORD RESET
# =============================================================

def request_password_reset(email: str):
    email = email.lower().strip()

    user = get_user_by_email(email)
    if user:
        token = send_auth_email(email, None)
        payload = {
            "token": token,
            "requested_at": time.time(),
            "expires_in": 600
        }
        r.setex(f"reset:{email}", 600, json.dumps(payload))

        return {
            "success": True,
            "message": "Reset code sent. Check your email.",
            "status": 200
        }

    else:
        return {
            "success": False,
            "message": f"Email {email} does not exist",
            "status": 404
        }


# =============================================================
# 2) VERIFY RESET TOKEN
# =============================================================

def verify_reset_token(email: str, token: str):
    email = email.lower().strip()

    entry = r.get(f"reset:{email}")
    if not entry:
        return {
            "success": False,
            "message": "No reset request found or token expired",
            "status": 404
        }

    data = json.loads(entry)

    if time.time() - data["requested_at"] > data["expires_in"]:
        r.delete(f"reset:{email}")
        return {
            "success": False,
            "message": "Token expired",
            "status": 400
        }

    if str(data["token"]) != str(token):
        return {
            "success": False,
            "message": "Invalid token",
            "status": 400
        }

    r.delete("reset_verified")
    r.setex("reset_verified", 600, email)

    print(f"✅ Verified reset token for: {email}")
    return {
        "success": True,
        "message": "Token verified successfully",
        "status": 200
    }


# =============================================================
# 3) RESET PASSWORD
# =============================================================

def reset_password(new_password: str):
    email = r.get("reset_verified")

    if not email:
        return {
            "success": False,
            "message": "No verified email stored",
            "status": 400
        }

    try:
        PasswordReset(email=email, password=new_password)
    except Exception as e:
        return {
            "success": False,
            "message": f"Invalid password: {str(e)}",
            "status": 400
        }

    updated = update_user_password(email, new_password)
    if not updated:
        return {
            "success": False,
            "message": "Database update failed",
            "status": 500
        }

    r.delete("reset_verified")
    r.delete(f"reset:{email}")

    print(f"✅ Password updated for {email}")
    return {
        "success": True,
        "message": "Password updated successfully",
        "status": 200
    }
