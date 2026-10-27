from datetime import datetime, timedelta, timezone
import bcrypt
from jose import jwt
from app.config import settings
from app.database.database import get_db

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, password_hash):
    return bcrypt.checkpw(password.encode(), password_hash.encode())

def create_access_token(user_id):
    exp = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode({"sub": str(user_id), "exp": exp}, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

def register_user(email, password):
    with get_db() as db:
        if db.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone():
            raise ValueError("Email already registered")
        cur = db.execute("INSERT INTO users(email,password_hash) VALUES(?,?)", (email, hash_password(password)))
        return {"id": cur.lastrowid, "email": email}

def authenticate_user(email, password):
    with get_db() as db:
        row = db.execute("SELECT id,email,password_hash FROM users WHERE email=?", (email,)).fetchone()
    if not row or not verify_password(password, row["password_hash"]):
        return None
    return {"id": row["id"], "email": row["email"]}
