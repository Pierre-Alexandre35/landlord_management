from fastapi import APIRouter, Depends, HTTPException
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer

from .schemas import RegisterSchema, LoginSchema, ChangePasswordSchema, TokenResponse
from .service import register_user, login_user, change_password
from .jwt_service import SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@router.post("/register", response_model=TokenResponse)
async def register(data: RegisterSchema):
    token = await register_user(data.email, data.password)
    return {"access_token": token}


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginSchema):
    token = await login_user(data.email, data.password)
    return {"access_token": token}


@router.post("/change-password")
async def change_pw(
    data: ChangePasswordSchema,
    user_id: str = Depends(get_current_user_id)
):
    await change_password(user_id, data.old_password, data.new_password)
    return {"status": "Password updated successfully"}
