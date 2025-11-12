# =============================================================
# PASSWORD RESET MANAGER
# =============================================================
import time
from crud import get_user_by_email, update_user_password
from schemas import PasswordReset
from mail.verify_email import send_auth_email
from mail.email_verification_manager import verify_token

# מאגר זמני לשמירת נתונים
pending_reset_emails = {}

# ✅ כאן נשמור את המייל שעבר אימות
verified_email_cache = { "email": None }


# =============================================================
# 1) בקשת איפוס סיסמה
# =============================================================

def request_password_reset(email: str):
    email = email.lower().strip()

    user = get_user_by_email(email)
    if not user:
        print(f"⚠️ Reset requested for NON-existing email: {email}")
        return {"success": True, "message": "If this email exists, a reset code was sent."}

    token = send_auth_email(email, None)

    pending_reset_emails[email] = {
        "token": token,
        "requested_at": time.time(),
        "expires_in": 600
    }

    print(f"✅ Sent reset token {token} to {email}")
    return {"success": True, "message": "Reset code sent. Check your email."}



# =============================================================
# 2) אימות טוקן
# =============================================================

def verify_reset_token(email: str, token: str):
    email = email.lower().strip()

    entry = pending_reset_emails.get(email)
    if not entry:
        return {"success": False, "message": "No reset request found"}

    # בדיקת פג תוקף
    if time.time() - entry["requested_at"] > entry["expires_in"]:
        pending_reset_emails.pop(email, None)
        return {"success": False, "message": "Token expired"}

    # ❗ בדיקת התאמת הטוקן (בלי verify_token של רישום!)
    if str(entry["token"]) != str(token):
        return {"success": False, "message": "Invalid token"}

    # ✅ כאן שומרים את המייל המאומת לשלב reset_password
    verified_email_cache["email"] = email

    print(f"✅ Verified reset token for: {email}")
    return {"success": True, "message": "Token verified successfully"}




# =============================================================
# 3) שינוי הסיסמה בפועל
# =============================================================

def reset_password(new_password: str):
    email = verified_email_cache.get("email")

    if not email:
        return {"success": False, "message": "No verified email stored"}

    try:
        PasswordReset(email=email, password=new_password)
    except Exception as e:
        return {"success": False, "message": f"Invalid password: {str(e)}"}

    updated = update_user_password(email, new_password)
    if not updated:
        return {"success": False, "message": "Database update failed"}

    # ✅ ניקוי הזיכרון
    verified_email_cache["email"] = None
    pending_reset_emails.pop(email, None)

    print(f"✅ Password updated for {email}")
    return {"success": True, "message": "Password updated successfully"}

