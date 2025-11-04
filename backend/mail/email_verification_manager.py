# =============================================================
# EMAIL VERIFICATION MANAGER
# =============================================================

import time

# =============================================================
# TEMPORARY STORAGE FOR PENDING VERIFICATIONS
# =============================================================

pending_verifications = {}


# =============================================================
# SAVE TOKEN
# =============================================================

def save_token(email, token, user_data, expires_in=600):
    """Saves the verification token and user data"""
    pending_verifications[email] = {
        "token": token,
        "data": user_data,
        "created_at": time.time(),
        "expires_in": expires_in
    }
    print(f"Token saved for {email}: {token}")


# =============================================================
# VERIFY TOKEN
# =============================================================

def verify_token(email, token):
    """Verifies whether a token matches and is still valid"""
    user_entry = pending_verifications.get(email)
    if not user_entry:
        return False, "No pending verification found"

    # Check expiration
    if (time.time() - user_entry["created_at"]) > user_entry["expires_in"]:
        pending_verifications.pop(email, None)
        return False, "Token expired"

    # Check token match
    if user_entry["token"] != token:
        return False, "Invalid token"

    user_data = user_entry["data"]
    pending_verifications.pop(email, None)
    return True, user_data
