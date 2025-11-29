import os
import asyncpg
from typing import Any, List, Optional, cast
from asyncpg import Pool, Record, Connection

pool: Optional[Pool] = None

DATABASE_URL = os.getenv("DATABASE_URL")


async def connect_to_db() -> None:
    """Create a global asyncpg pool."""
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)


async def disconnect_from_db() -> None:
    """Close the global pool."""
    global pool
    if pool is not None:
        await pool.close()


async def poolfetchrow(query: str, *args: Any) -> Optional[Record]:
    if pool is None:
        raise RuntimeError("Database pool is not initialized")

    async with pool.acquire() as raw_conn:
        conn = cast(Connection, raw_conn)
        return await conn.fetchrow(query, *args)


async def poolexecute(query: str, *args: Any) -> str:
    if pool is None:
        raise RuntimeError("Database pool is not initialized")

    async with pool.acquire() as raw_conn:
        conn = cast(Connection, raw_conn)
        return await conn.execute(query, *args)


async def poolfetch(query: str, *args: Any) -> List[Record]:
    if pool is None:
        raise RuntimeError("Database pool is not initialized")

    async with pool.acquire() as raw_conn:
        conn = cast(Connection, raw_conn)
        rows: List[Record] = await conn.fetch(query, *args)
        return rows
