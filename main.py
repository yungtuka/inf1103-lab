import json
import os

from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from product_factory import create_product_from_dict
from inventory import Inventory

INVENTORY_FILE = "inventory.json"


# ---------- File handling (load / save) ----------
def load_inventory():
    inventory = Inventory()
    if os.path.exists(INVENTORY_FILE):
        try:
            with open(INVENTORY_FILE, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print(f"{INVENTORY_FILE} is not valid JSON. Starting with an empty inventory.")
            return inventory
        for item in data:
            try:
                # Lab 7: the "type" field decides which subclass is created
                product = create_product_from_dict(item)
            except (KeyError, ValueError) as error:
                print(f"Skipped an entry that could not be loaded: {error}")
                continue
            inventory.add_product(product)
        print(f"{INVENTORY_FILE} found. Inventory loaded successfully.")
    else:
        print(f"{INVENTORY_FILE} not found. Starting with an empty inventory.")
    return inventory


def save_inventory(inventory):
    # Lab 7: each product builds its own dictionary (incl. type + extra field)
    data = [product.to_dict() for product in inventory.get_products()]
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


def add_product_flow(inventory):
    print("\nAdd a new product")
    print("  1. Physical product")
    print("  2. Digital product")
    product_type = input("Choose product type (1-2): ").strip()
    if product_type not in ("1", "2"):
        print("Invalid product type. Product was not added.")
        return

    pid = input("Product ID: ").strip()
    name = input("Product Name: ").strip()
    if not pid or not name:
        print("Product ID and name cannot be empty. Product was not added.")
        return
    try:
        price = float(input("Product Price: ").strip())
        stock = int(input("Product Stock: ").strip())
        if price < 0 or stock < 0:
            print("Price and stock cannot be negative. Product was not added.")
            return
        if product_type == "1":
            weight = float(input("Weight (kg): ").strip())
            if weight <= 0:
                print("Weight must be greater than 0. Product was not added.")
                return
            product = PhysicalProduct(pid, name, price, stock, weight)
        else:
            download_size = float(input("Download size (MB): ").strip())
            if download_size <= 0:
                print("Download size must be greater than 0. Product was not added.")
                return
            product = DigitalProduct(pid, name, price, stock, download_size)
    except ValueError:
        print("Invalid number entered. Product was not added.")
        return

    if inventory.add_product(product):
        print("Product added successfully.")
    else:
        print(f"Product with ID {pid} already exists.")


def main():
    print("--- Inventory Management System ---")
    inventory = load_inventory()

    while True:
        show_menu()
        choice = input("Enter option: ").strip()

        if choice == "1":
            inventory.display_all()

        elif choice == "2":
            add_product_flow(inventory)

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
                print(f"    {product.get_fulfilment_info()}")
                # Only objects that signed the CanBeShipped contract have this
                if isinstance(product, CanBeShipped):
                    print(f"    Shipping cost: ${product.calculate_shipping_cost():.2f}")

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
