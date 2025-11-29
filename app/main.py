from fastapi import FastAPI
import app.db as db
from app.auth.routes import router as auth_router

app = FastAPI()

@app.on_event("startup")
async def startup():
    await db.connect_to_db()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect_from_db()

app.include_router(auth_router)

@app.get("/")
async def hello():
    return {"message": "Hello World from FastAPI with PostgreSQL!"}

@app.get("/db-check")
async def db_check():
    if db.pool is None:
        return {"status": "pool is None — DB not connected"}

    try:
        async with db.poolacquire() as conn:
            await conn.execute("SELECT 1;")
        return {"status": "Connected to database!"}

    except Exception as e:
        return {"status": "Failed to query DB", "error": str(e)}
