from config.redis_client import redis_client

ORDER_SOURCE_KEY = "order_source:{order_id}"


async def set_order_source(order_id: int, source: str, ttl: int = 3600):
    key = ORDER_SOURCE_KEY.format(order_id=order_id)
    await redis_client.set(key, source, ex=ttl)


async def get_order_source(order_id: int) -> str:
    key = ORDER_SOURCE_KEY.format(order_id=order_id)
    source = await redis_client.get(key)

    if not source:
        return "prod"  # fail-safe

    return source.decode() if isinstance(source, bytes) else source


def normalize_source(source: str | None) -> str:
    if not source:
        return "prod"

    source = source.strip().lower()

    if source not in ("stage", "prod"):
        return "prod"

    return source