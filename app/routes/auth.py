from app.db.session import get_db
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from fastapi import APIRouter, HTTPException, Depends, Response
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session

from app.routes.user import get_current_user

router = APIRouter()

class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

    @field_validator("password")
    @classmethod
    def password_length(cls, v):
        if len(v.encode("utf-8")) > 72:
            raise HTTPException(
                status_code=400,
                detail="Password too long (max 72 bytes)"
            )
        return v


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == data.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    print(existing_user)

    new_user = User(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        password_hash=hash_password(data.password)  
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created"}


@router.post("/login")
def login(data: dict, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data["email"]).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(data["password"], str(user.password_hash)):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})

    return {"access_token": token, "token_type": "bearer"}

@router.get("/auth/me")
def me(user: User = Depends(get_current_user)):
    return {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    }