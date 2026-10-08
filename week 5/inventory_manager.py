import json
import os

INVENTORY_FILE = "inventory.json"

def load_inventory(filename=INVENTORY_FILE):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            inventory = json.load(f)
        print(f"{filename} found. Inventory loaded successfully.")
        return inventory
    print(f"{filename} not found. Starting with an empty inventory.")
    return []

        

def find_product(inventory, product_id):
    for product in inventory:
        if product["id"] == product_id:
            return product
    return None

def add_product(inventory, product_id, name, price, stock):
    if find_product(inventory, product_id) is not None:
        return False
    inventory.append({
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock
    })
    return True

def update_stock(inventory, product_id, new_stock):
    product = find_product(inventory, product_id)
    if product is None:
        return None
    product["stock"] = new_stock
    return product

def search_product(inventory, product_id):
    return find_product(inventory, product_id)

def display_all(inventory):
    print("----Current Inventory----")
    if not inventory:
        print("The inventory is empty.")
    else:
        for product in inventory:
            print(f"ID: {product['id']} | Name: {product['name']} | "
                  f"Price: ${product['price']:.2f} | Stock: {product['stock']}")
    print("-------------------------")


inv = []
add_product(inv, "P001", "Laptop", 1200.00, 15)
add_product(inv, "P002", "Mouse", 25.50, 40)
add_product(inv, "P003", "Keyboard", 45.00, 25)
display_all(load_inventory())
