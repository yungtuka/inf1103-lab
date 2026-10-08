import json
import os

INVENTORY_FILE = "inventory.json"

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


def load_inventory():
    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, "r") as f:
            inventory = json.load(f)
        print(f"{INVENTORY_FILE} found. Inventory loaded successfully.")
        return inventory
    print(f"{INVENTORY_FILE} not found. Starting with an empty inventory.")
    return []

def save_inventory(inventory):
    with open(INVENTORY_FILE, "w") as f:
        json.dump(inventory, f, indent=4)
    print("Inventory saved successfully.")

def show_menu():
    print("\n---- MENU ----")
    print("1. Display all products")
    print("2. Add a new product")
    print("3. Update stock of a product")
    print("4. Search for a product")
    print("5. Save inventory")
    print("6. Exit")
    print("----------------")

def main():
    print("--- Inventory Management System ---")
    inventory = load_inventory()

    while True:
        show_menu()
        choice = input("Enter option: ").strip()

        if choice == "1":   
            display_all(inventory)
        elif choice == "2":
            print("\n Add a new product")
            pid = input("Product ID: ").strip()
            name = input("Product Name: ").strip()
            try:
                price = float(input("Product Price: ").strip())
                stock = int(input("Product Stock: ").strip())
            except ValueError:
                print("Invalid input for price or stock. Product was not added.")
                continue
            if add_product(inventory, pid, name, price, stock):
                print(f"Product added successfully.")
            else:
                print(f"Product with ID {pid} already exists. ")
        elif choice == "3":
            print("\n Update stock of a product")
            pid = input("Product ID: ").strip()
            product = search_product(inventory, pid)
            if product is None:
                print(f"Product was not found.")
                continue
            print("Product Found: ")
            print(f"Name: {product['name']}")
            print(f"Current Stock: {product['stock']}")
            try:
                new_stock = int(input("Enter new stock quantity: ").strip())
            except ValueError:
                print("Invalid input for stock. Stock was not updated.")
                continue
            update_stock(inventory, pid, new_stock)
            print(f"Stock updated successfully.")
        elif choice == "4":
            print("\nSearch Product")
            pid = input("Enter Product ID: ").strip()
            product = search_product(inventory, pid)
            if product is None:
                print("Product not found.")
            else:
                print("Product Found")
                print("-----")
                print(f"ID: {product['id']}")
                print(f"Name: {product['name']}")
                print(f"Price: ${product['price']:.2f}")
                print(f"Stock: {product['stock']}")
                print("-----")

        elif choice == "5":
            print("Saving inventory...")
            save_inventory(inventory)

        elif choice == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break

        else:
            print("Invalid option. Please enter 1-6.")

if __name__ == "__main__":
    main()


inv = []
add_product(inv, "P001", "Laptop", 1200.00, 15)
add_product(inv, "P002", "Mouse", 25.50, 40)
add_product(inv, "P003", "Keyboard", 45.00, 25)
add_product(inv, "P004", "Monitor", 299.00, 10)
display_all(inv)
