import asyncpg, asyncio

async def _update_tree(conn, tree_id, common_name, some_param):
    await conn.execute("""
        UPDATE Trees
        SET common_name = $1, some_field = $2
        WHERE tree_id = $3;
    """, common_name, some_param, tree_id)

def update_tree(pool, *, tree_id, common_name, some_param):
    asyncio.get_event_loop().run_until_complete(
        _update_tree(pool, tree_id, common_name, some_param)
    )
