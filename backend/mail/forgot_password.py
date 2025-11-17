# =============================================================
# PASSWORD RESET MANAGER — REDIS VERSION
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
    host="redis",   # חשוב! localhost לבדיקה
    port=6379,
    decode_responses=True
)


# =============================================================
# 1) בקשת איפוס סיסמה
# =============================================================

def request_password_reset(email: str):
    email = email.lower().strip()

    user = get_user_by_email(email)
    if not user:
        print(f"⚠️ Reset requested for NON-existing email: {email}")
        return {"success": True, "message": "If this email exists, a reset code was sent."}

    # שליחת הטוקן למייל (כמו קודם)
    token = send_auth_email(email, None)

    # יצירת Payload
    payload = {
        "token": token,
        "requested_at": time.time(),
        "expires_in": 600
    }

    # שמירה ב־Redis ל־10 דקות
    r.setex(f"reset:{email}", 600, json.dumps(payload))

    print(f"✅ Sent reset token {token} to {email}")
    return {"success": True, "message": "Reset code sent. Check your email."}



# =============================================================
# 2) אימות טוקן
# =============================================================

def verify_reset_token(email: str, token: str):
    email = email.lower().strip()

    entry = r.get(f"reset:{email}")
    if not entry:
        return {"success": False, "message": "No reset request found or token expired"}

    data = json.loads(entry)

    # בדיקת תוקף
    if time.time() - data["requested_at"] > data["expires_in"]:
        r.delete(f"reset:{email}")
        return {"success": False, "message": "Token expired"}

    # בדיקת טוקן
    if str(data["token"]) != str(token):
        return {"success": False, "message": "Invalid token"}

    # שמירת המייל המאומת (שימוש בשלב reset_password)
    r.setex("reset_verified", 600, email)

    print(f"✅ Verified reset token for: {email}")
    return {"success": True, "message": "Token verified successfully"}



# =============================================================
# 3) שינוי הסיסמה בפועל
# =============================================================

def reset_password(new_password: str):
    email = r.get("reset_verified")

    if not email:
        return {"success": False, "message": "No verified email stored"}

    # Validate password using schema
    try:
        PasswordReset(email=email, password=new_password)
    except Exception as e:
        return {"success": False, "message": f"Invalid password: {str(e)}"}

    # Update DB
    updated = update_user_password(email, new_password)
    if not updated:
        return {"success": False, "message": "Database update failed"}

    # Clear Redis keys
    r.delete("reset_verified")
    r.delete(f"reset:{email}")

    print(f"✅ Password updated for {email}")
    return {"success": True, "message": "Password updated successfully"}
