# =============================================================
# EMAIL VERIFICATION MANAGER — REDIS VERSION
# =============================================================

import json
import redis

# =============================================================
# CONNECT TO REDIS (via docker-compose service name)
# =============================================================

r = redis.StrictRedis(
    host="redis",
    port=6379,
    decode_responses=True
)



# =============================================================
# SAVE TOKEN
# =============================================================

def save_token(email, token, user_data, expires_in=600):
    """
    Saves the verification token + user data into Redis
    with expiration time (TTL)
    """

    payload = {
        "token": token,
        "data": user_data
    }

    # שמירה עם תוקף אוטומטי (Redis מוחק לבד אחרי 600 שניות)
    r.setex(f"verify:{email}", expires_in, json.dumps(payload))

    print(f"[Redis] Token saved for {email}: {token}")


# =============================================================
# VERIFY TOKEN
# =============================================================

def verify_token(email, token):
    """
    Verifies whether a token matches and is still valid.
    Automatically deletes key after successful verification.
    """

    entry = r.get(f"verify:{email}")

    if not entry:
        return False, "No pending verification or token expired"

    payload = json.loads(entry)

    # Check token
    if payload["token"] != token:
        return False, "Invalid token"

    # Extract user data
    user_data = payload["data"]

    # מחיקה אחרי אימות מוצלח
    r.delete(f"verify:{email}")

    return True, user_data
