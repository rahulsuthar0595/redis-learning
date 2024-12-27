import asyncio

import redis as red


async def main():
    conn = red.Redis(host="localhost", port=6379, decode_responses=True)

    publish(conn, 1, 'Hello'),
    publish(conn, 2, 'New Notification'),
    publish(conn, 2, 'HIII')


def publish(redis, channel, message):
    return redis.publish(f'broadcast:channel:{channel}', message)


asyncio.run(main())
