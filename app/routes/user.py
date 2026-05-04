from fastapi import APIRouter, Depends, HTTPException, Cookie
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from app.core.config import SECRET_KEY, ALGORITHM
from app.db.session import get_db
from app.models.user import User
from sqlalchemy.orm import Session

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email = payload["sub"]

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")

    return user
