import redis

# conn = redis.from_url("redis://default:MM3RYKvZFw5drP2kMJb7WH1ELDD2DkhY@redis-13189.c301.ap-south-1-1.ec2.redns.redis-cloud.com:13189")
# conn = redis.Redis(
#     host='redis-13189.c301.ap-south-1-1.ec2.redns.redis-cloud.com',
#     port=13189,
#     decode_responses=True,
#     username="default",
#     password="MM3RYKvZFw5drP2kMJb7WH1ELDD2DkhY",
# )

conn = redis.Redis(host="localhost", port=6379, decode_responses=True)

print(conn.ping())  # True

res = conn.set(name="email", value="rahul@mindinventory.com")
print(res)  # True

res = conn.set(name="email", value="suthar@mindinventory.com", get=True)
print(res)  # Return old value : rahul@mindinventory.com

res = conn.set(name="new_email", value="suthar@mindinventory.com", get=True)
print(res)  # Return None if old value not present for the key

res = conn.get(name="email")
print(res)  # suthar@mindinventory.com

# Data Structure:

# 1. List

res = conn.keys()
print(res)

res = conn.lpush("Favourite Game", *["Chess", "Cricket", "Badminton"])  # Push value at start
print(res)  # Return total count : 3

res = conn.lrange("Favourite Game", 0, 1)
print(res)  # Return in reverse order: ['Badminton', 'Cricket']

res = conn.rpush("Favourite Game", *["Pool"])
print(res)  # Return total count : 4

res = conn.llen("Favourite Game")
print(res)  # 4


# 2. String

res = conn.set("Address", "Gujarat")
print(res)  # True

res = conn.get("Address")
print(res)  # Gujarat

res = conn.get("Invalid-Address")
print(res)  # None

res = conn.mset({"name": "Rahul", "age": 23})
print(res)  # True

res = conn.mget(["name", "age"])
print(res)  # ['Rahul', '23']

res = conn.incrby("age", 1)
print(res)  # 24

res = conn.getdel("age")
print(res)  # 24 , remove value of key and return value

res = conn.strlen("name")
print(res)  # 5


# 3. Hash Data Type: Store key-value pairs


res = conn.hset(name="session", mapping={"name": "Rahul", "age": 23})
print(res)  # 1

res = conn.hget(name="session", key="name")
print(res)  # Rahul

res = conn.hget(name="invalid-session", key="name")
print(res)  # None

res = conn.hgetall(name="session")
print(res)  # {'name': 'Rahul', 'age': '23'}




# 4. GeoSpatial

res = conn.geoadd("bikes:rentable",  [-122.27652, 37.805186, "station:1"])
print(res)  # # >>> 1

res2 = conn.geoadd("bikes:rentable", [-122.2674626, 37.8062344, "station:2"])
print(res2)  # >>> 1

res3 = conn.geoadd("bikes:rentable", [-122.2469854, 37.8104049, "station:3"])
print(res3)  # >>> 1

res4 = conn.geosearch(
    "bikes:rentable",
    longitude=-122.27652,
    latitude=37.805186,
    radius=5,
    unit="km",
)
print(res4)
