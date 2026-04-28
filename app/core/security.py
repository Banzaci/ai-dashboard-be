from bcrypt import gensalt, hashpw
from jose import jwt
from passlib.context import CryptContext
from app.core.config import SECRET_KEY, ALGORITHM

pwd = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(pw: str):
    return pwd.hash(pw)

def verify_password(pw: str, hashed: str):
    """Verify a password against its hash."""
    return pwd.verify(pw, hashed)

def create_access_token(data: dict):
    """Create a JWT token from data."""
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    """Decode a JWT token."""
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
