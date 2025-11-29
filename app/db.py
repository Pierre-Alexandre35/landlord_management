import asyncpg
import os

pool = None

DATABASE_URL = os.getenv("DATABASE_URL")

async def connect_to_db():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)

async def disconnect_from_db():
    global pool
    if pool:
        await pool.close()


async def poolfetchrow(query, *args):
    async with pool.acquire() as conn:
        return await conn.fetchrow(query, *args)

async def poolexecute(query, *args):
    async with pool.acquire() as conn:
        return await conn.execute(query, *args)

async def poolfetch(query, *args):
    async with pool.acquire() as conn:
        return await conn.fetch(query, *args)
