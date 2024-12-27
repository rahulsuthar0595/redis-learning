import asyncio

import redis as red


async def main():
    conn = red.Redis(host="localhost", port=6379, decode_responses=True)
    pubsub = conn.pubsub()

    channel = pubsub.psubscribe('broadcast:channel:*')

    for message in pubsub.listen():
        # Ignore subscription confirmation message

        if message['type'] == 'psubscribe':
            continue
        print(f"Received message: {message['data']}")



asyncio.run(main())
