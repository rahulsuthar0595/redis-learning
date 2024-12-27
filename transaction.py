import time
from multiprocessing import Process

import redis

conn = redis.Redis(host='localhost', port=6379, decode_responses=True)


def initialize_data():
    conn.set('inventory:shirt', 10)  # set value to 10
    conn.set('cart:user1', 0)  # default cart quantity 0
    print("initialize_data executed.")


def add_to_cart(user_id, product_id, quantity):
    try:
        with conn.pipeline() as transaction:
            # Watch the inventory for concurrent changes
            transaction.watch(f'inventory:{product_id}')
            print("Client 1: Watching inventory.")

            time.sleep(3)  # Allow Client 2 to modify during this delay

            stock = int(conn.get(f'inventory:{product_id}'))

            if stock < quantity:
                raise ValueError("stock insufficient.")

            cart_quantity = int(conn.get(f'cart:{user_id}') or 0)

            # Start the transaction
            transaction.multi()

            # Update the cart and inventory
            transaction.set(f'cart:{user_id}', cart_quantity + quantity)
            transaction.set(f'inventory:{product_id}', stock - quantity)

            # Execute the transaction atomically
            transaction.execute()

            print(f"Successfully added {quantity} of {product_id} to {user_id}'s cart.")

    except redis.exceptions.WatchError:
        print(f"Transaction failed for {user_id}: Inventory was modified.")
    except ValueError as e:
        print(f"Error for {user_id}: {e}")


def modify_inventory(product_id):
    time.sleep(1)  # Ensure it happens during Client 1's transaction
    conn.set(f'inventory:{product_id}', 50)  # Modify inventory
    print(f"Client 2: Modified inventory for {product_id}.")


if __name__ == "__main__":
    initialize_data()

    # Run Client 1 and Client 2 as separate processes
    client1_process = Process(target=add_to_cart, args=('user1', 'product1', 2))
    client2_process = Process(target=modify_inventory, args=('product1',))

    # Start both processes
    client1_process.start()
    client2_process.start()

    # Wait for both processes to finish
    client1_process.join()
    client2_process.join()
