import aioredis


async def open_redis_connection(app, loop):
    minsize = getattr(app.config, 'REDIS_POOL_MINSIZE', 5)
    maxsize = getattr(app.config, 'REDIS_POOL_MAXSIZE', 10)
    app.redis_client = await aioredis.create_pool(
        app.config.REDIS_URL,
        loop=loop,
        minsize=minsize,
        maxsize=maxsize)


async def close_redis_connection(app, loop):
    app.redis_client.close()
