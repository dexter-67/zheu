import json
import os

import aio_pika


RABBITMQ_URL = os.getenv(
    "RABBITMQ_URL",
    "amqp://guest:guest@rabbitmq:5672/",
)


async def publish_event(
    queue_name: str,
    payload: dict,
):
    connection = await aio_pika.connect_robust(RABBITMQ_URL)

    async with connection:
        channel = await connection.channel()

        queue = await channel.declare_queue(
            queue_name,
            durable=True,
        )

        message = aio_pika.Message(
            body=json.dumps(payload).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )

        await channel.default_exchange.publish(
            message,
            routing_key=queue.name,
        )
