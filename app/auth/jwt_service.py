from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "CHANGE_THIS_VERY_SECRET_KEY"   # put env var later!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

def create_access_token(payload: dict):
    to_encode = payload.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
