import bcrypt

def hash_password(plain_password: str) -> str:
    pw_bytes = plain_password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw_bytes, salt).decode('utf-8')
