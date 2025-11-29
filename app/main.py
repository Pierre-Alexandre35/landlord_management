from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from asyncpg import Connection
from typing import cast

import app.db as db
from app.auth.routes import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect_to_db()
    yield
    await db.disconnect_from_db()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)


@app.get("/")
async def hello():
    return {"message": "Hello World from FastAPI with PostgreSQL!"}


@app.get("/db-check")
async def db_check():
    if db.pool is None:
        return {"status": "pool is None — DB not connected"}

    try:
        async with db.pool.acquire() as raw_conn:
            conn = cast(Connection, raw_conn)
            await conn.execute("SELECT 1;")
        return {"status": "Connected to database!"}

    except Exception as e:
        return {"status": "Failed to query DB", "error": str(e)}
