import redis
from redis.cluster import ClusterNode
from redis.exceptions import RedisClusterException

redis_cluster = redis.cluster.RedisCluster(
    startup_nodes=[ClusterNode(host="localhost", port=30001), ClusterNode(host="localhost", port=30002)],
    decode_responses=True
)


def add_to_cart(user_id, item_id, quantity):
    try:
        cart_key = f"cart:{user_id}"
        redis_cluster.hset(cart_key, item_id, quantity)
        print(f"Item {item_id} added to cart for user {user_id} with quantity {quantity}")
    except RedisClusterException as e:
        print(f"Error adding item to cart: {e}")


def get_cart(user_id):
    try:
        cart_key = f"cart:{user_id}"
        cart_items = redis_cluster.hgetall(cart_key)
        return cart_items
    except RedisClusterException as e:
        print(f"Error fetching cart for user {user_id}: {e}")
        return {}


# # Example usage
# add_to_cart(101, "item_123", 2)  # User 101 adds 2 units of item_123 to their cart
# add_to_cart(101, "item_456", 1)  # User 101 adds 1 unit of item_456 to their cart

cart = get_cart(101)
print(f"User 101's cart: {cart}")
