import hashlib
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import HTTPException, Request, Depends
from database import SessionLocal
import crud, schemas
from sqlalchemy.orm import Session

SECRET_KEY = "YOUR_SECRET_KEY" 
ALGORITHM = "HS256"

# Use Argon2 hashing scheme
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def sha256_hash(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def get_password_hash(password: str) -> str:
    # Pre-hash with SHA256 then Argon2
    pre_hashed = sha256_hash(password)
    return pwd_context.hash(pre_hashed)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    pre_hashed = sha256_hash(plain_password)
    return pwd_context.verify(pre_hashed, hashed_password)

def authenticate_user(db: Session, email: str, password: str):
    user = crud.get_user_by_email(db, email)
    if not user or not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict):
    from datetime import datetime, timedelta
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=6)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(request: Request, db=Depends(lambda: SessionLocal())):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user = crud.get_user_by_email(db, email)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return schemas.UserOut.from_orm(user)
    except JWTError:
        raise HTTPException(status_code=401, detail="Not authenticated")



