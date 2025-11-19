# =============================================================
# EMAIL VERIFICATION MANAGER — REDIS VERSION
# =============================================================

import json
import redis

# =============================================================
# CONNECT TO REDIS (via docker-compose service name)
# =============================================================

r = redis.StrictRedis(
    host="redis",      # Redis service name from docker-compose
    port=6379,
    decode_responses=True
)


# =============================================================
# SAVE TOKEN
# =============================================================

def save_token(email, token, user_data, expires_in=600):
    """
    Saves the verification token and user data into Redis.
    Data is stored with a TTL (expires_in), meaning Redis   
    will automatically delete it when time is up.
    """

    payload = {
        "token": token,
        "data": user_data
    }

    # Store in Redis with automatic expiration
    r.setex(f"verify:{email}", expires_in, json.dumps(payload))

    print(f"[Redis] Token saved for {email}: {token}")


# =============================================================
# VERIFY TOKEN
# =============================================================

def verify_token(email, token):
    """
    Verifies whether the token matches and is still valid.
    Returns (success: bool, message or user_data).
    Automatically deletes the Redis entry when verification succeeds.
    """

    entry = r.get(f"verify:{email}")

    # No data means no pending verification / expired token
    if not entry:
        return False, "No pending verification or token expired"

    payload = json.loads(entry)

    # Token mismatch
    if payload["token"] != token:
        return False, "Invalid token"

    # Extract stored user data (will be passed to the registration flow)
    user_data = payload["data"]

    # Clean up after successful verification
    r.delete(f"verify:{email}")

    return True, user_data
