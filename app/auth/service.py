from fastapi import HTTPException
from app.db import poolfetchrow, poolexecute
from .hash import hash_password, verify_password
from .jwt_service import create_access_token


async def register_user(email: str, password: str):
    existing = await poolfetchrow(
        "SELECT id FROM users WHERE email = $1;", email
    )
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(password)

    row = await poolfetchrow(
        """
        INSERT INTO users (email, password_hash)
        VALUES ($1, $2)
        RETURNING id, email;
        """,
        email, hashed
    )

    token = create_access_token({"sub": str(row["id"])})
    return token


async def login_user(email: str, password: str):
    user = await poolfetchrow(
        "SELECT id, password_hash FROM users WHERE email = $1;",
        email
    )
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(password, user["password_hash"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": str(user["id"])})
    return token


async def change_password(user_id: str, old_password: str, new_password: str):
    user = await poolfetchrow(
        "SELECT password_hash FROM users WHERE id = $1;",
        user_id
    )

    if not user or not verify_password(old_password, user["password_hash"]):
        raise HTTPException(status_code=400, detail="Incorrect current password")

    new_hash = hash_password(new_password)

    await poolexecute(
        "UPDATE users SET password_hash = $1 WHERE id = $2;",
        new_hash, user_id
    )
