import json
import redis.asyncio as redis

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

ORDER_KEY = "tg:order:{order_id}"


async def save_order_message(order_id: int, chat_id: int, message_id: int, text: str):
    key = ORDER_KEY.format(order_id=order_id)
    await redis_client.set(
        key,
        json.dumps({
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text
        }),
        ex=60 * 60 * 3  # 3 часов TTL
    )


async def get_order_message(order_id: int):
    key = ORDER_KEY.format(order_id=order_id)
    data = await redis_client.get(key)
    return json.loads(data) if data else None


async def delete_order_message(order_id: int):
    key = ORDER_KEY.format(order_id=order_id)
    print(key)
    await redis_client.delete(key)