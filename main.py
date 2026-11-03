import json
import os

from product import Product
from inventory import Inventory

INVENTORY_FILE = "inventory.json"


# ---------- File handling (load / save) ----------
def load_inventory():
    inventory = Inventory()
    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, "r") as f:
            data = json.load(f)
        for item in data:
            product = Product(item["id"], item["name"], item["price"], item["stock"])
            inventory.add_product(product)
        print(f"{INVENTORY_FILE} found. Inventory loaded successfully.")
    else:
        print(f"{INVENTORY_FILE} not found. Starting with an empty inventory.")
    return inventory


def save_inventory(inventory):
    data = []
    for product in inventory.get_products():
        data.append({
            "id": product.get_product_id(),
            "name": product.get_name(),
            "price": product.get_price(),
            "stock": product.get_stock(),
        })
    with open(INVENTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print("Inventory saved successfully.")


# ---------- Menu / user input ----------
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
            inventory.display_all()

        elif choice == "2":
            print("\nAdd a new product")
            pid = input("Product ID: ").strip()
            name = input("Product Name: ").strip()
            try:
                price = float(input("Product Price: ").strip())
                stock = int(input("Product Stock: ").strip())
            except ValueError:
                print("Invalid input for price or stock. Product was not added.")
                continue
            product = Product(pid, name, price, stock)
            if inventory.add_product(product):
                print("Product added successfully.")
            else:
                print(f"Product with ID {pid} already exists.")

        elif choice == "3":
            print("\nUpdate stock of a product")
            pid = input("Product ID: ").strip()
            product = inventory.search_product(pid)
            if product is None:
                print("Product was not found.")
                continue
            print("Product Found:")
            print(f"Name: {product.get_name()}")
            print(f"Current Stock: {product.get_stock()}")
            try:
                new_stock = int(input("Enter new stock quantity: ").strip())
            except ValueError:
                print("Invalid input for stock. Stock was not updated.")
                continue
            product.update_stock(new_stock)

        elif choice == "4":
            print("\nSearch Product")
            pid = input("Enter Product ID: ").strip()
            product = inventory.search_product(pid)
            if product is None:
                print("Product not found.")
            else:
                print("Product Found")
                product.display_information()

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
