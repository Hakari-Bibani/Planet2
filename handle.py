import asyncpg, asyncio, os
import streamlit as st

# Cache the connection pool so it's not re-created on each run
@st.cache_resource
def init_db_pool():
    """Initialize and return an asyncpg connection pool."""
    # Read connection info from environment or config
    db_url = os.getenv("DATABASE_URL")  # e.g., "postgresql://user:pass@host/db?sslmode=require"
    return asyncio.get_event_loop().run_until_complete(
        asyncpg.create_pool(dsn=db_url, min_size=1, max_size=10)
    )

# CRUD Operations for Trees
async def _insert_tree(conn, common_name, scientific_name, shape, watering, photo_url,
                       origin, soil, root, leaf, growth):
    await conn.execute("""
        INSERT INTO Trees(common_name, scientific_name, shape, Watering_demand, Main_Photo_url,
                          Origin, Soil_type, Root_type, Leaf_Type, Growth_rate)
        VALUES($1,$2,$3,$4,$5,$6,$7,$8,$9,$10);
    """, common_name, scientific_name, shape, watering, photo_url,
         origin, soil, root, leaf, growth)

def add_tree(pool, **tree_data):
    """Add a new tree record to the database."""
    # Run the async insertion in an event loop
    asyncio.get_event_loop().run_until_complete(
        _use_connection(pool, _insert_tree, **tree_data)
    )

async def _use_connection(pool, coro_func, **kwargs):
    """Helper to acquire a connection from the pool and execute an async function."""
    async with pool.acquire() as conn:
        # Inside this, call the provided coroutine with the connection
        await coro_func(conn, **kwargs)

def get_all_trees(pool):
    """Fetch all trees as a list of dictionaries."""
    async def _fetch(conn):
        return await conn.fetch("SELECT * FROM Trees;")
    records = asyncio.get_event_loop().run_until_complete(
        _use_connection(pool, lambda conn: conn.fetch("SELECT * FROM Trees;"))
    )
    # convert records (asyncpg.Record) to list of dicts for easier use
    return [dict(r) for r in records]

# Similar functions: update_tree, delete_tree, and corresponding functions for Nurseries and Inventory...
