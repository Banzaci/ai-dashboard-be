from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from app.core.config import SECRET_KEY, ALGORITHM

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
      payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
      return payload["sub"]
    except:
      raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/me")
def me(user: str = Depends(get_current_user)):
    return {"user": user}