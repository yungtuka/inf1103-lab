import json
import os

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from product_factory import create_product_from_dict
from inventory import Inventory
from order import Order

INVENTORY_FILE: str = "inventory.json"


# ---------- File handling (load / save) ----------
def load_inventory() -> tuple[Inventory, dict[str, Supplier]]:
    """Load suppliers first, then products that refer to them."""
    inventory = Inventory()
    suppliers: dict[str, Supplier] = {}

    if not os.path.exists(INVENTORY_FILE):
        print(f"{INVENTORY_FILE} not found. Starting with an empty inventory.")
        return inventory, suppliers

    try:
        with open(INVENTORY_FILE, "r") as f:
            data = json.load(f)
        supplier_data = data["suppliers"]
        product_data = data["products"]
    except (json.JSONDecodeError, KeyError, TypeError):
        print(f"{INVENTORY_FILE} is not in the Lab 8 format. Starting with an empty inventory.")
        return inventory, suppliers

    # 1. Suppliers are created on their own (they exist independently)
    for item in supplier_data:
        supplier = Supplier.from_dict(item)
        suppliers[supplier.get_supplier_id()] = supplier

    # 2. Each product is given a reference to its existing Supplier
    for item in product_data:
        supplier = suppliers.get(item.get("supplier_id"))
        if supplier is None:
            print(f"Skipped product {item.get('id')}: unknown supplier.")
            continue
        try:
            product = create_product_from_dict(item, supplier)
        except (KeyError, ValueError) as error:
            print(f"Skipped an entry that could not be loaded: {error}")
            continue
        inventory.add_product(product)

    print(f"{INVENTORY_FILE} found. Inventory loaded successfully.")
    return inventory, suppliers


def save_inventory(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    data = {
        "suppliers": [supplier.to_dict() for supplier in suppliers.values()],
        "products": [product.to_dict() for product in inventory.get_products()],
    }
    with open(INVENTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print("Inventory saved successfully.")


# ---------- Menu / user input ----------
def show_menu() -> None:
    print("\n---- MENU ----")
    print("1. Display all products")
    print("2. Add a new product")
    print("3. Update stock of a product")
    print("4. Search for a product")
    print("5. Remove a product")
    print("6. Add a supplier")
    print("7. Display all suppliers")
    print("8. Create an order")
    print("9. Save inventory")
    print("10. Exit")
    print("----------------")


def display_suppliers(suppliers: dict[str, Supplier]) -> None:
    print("----Suppliers----")
    if not suppliers:
        print("No suppliers yet.")
    for supplier in suppliers.values():
        supplier.display_information()
    print("-----------------")


def add_supplier_flow(suppliers: dict[str, Supplier]) -> None:
    print("\nAdd a supplier")
    supplier_id = input("Supplier ID: ").strip()
    name = input("Supplier Name: ").strip()
    email = input("Contact Email: ").strip()
    if not supplier_id or not name or not email:
        print("Supplier ID, name and email cannot be empty. Supplier was not added.")
        return
    if supplier_id in suppliers:
        print(f"Supplier with ID {supplier_id} already exists.")
        return
    suppliers[supplier_id] = Supplier(supplier_id, name, email)
    print("Supplier added successfully.")


def add_product_flow(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    print("\nAdd a new product")
    if not suppliers:
        print("Please add a supplier first (option 6).")
        return
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

    print("Available suppliers: " + ", ".join(suppliers.keys()))
    supplier = suppliers.get(input("Supplier ID: ").strip())
    if supplier is None:
        print("Supplier not found. Product was not added.")
        return

    try:
        price = float(input("Product Price: ").strip())
        stock = int(input("Product Stock: ").strip())
        if price < 0 or stock < 0:
            print("Price and stock cannot be negative. Product was not added.")
            return
        product: Product
        if product_type == "1":
            weight = float(input("Weight (kg): ").strip())
            if weight <= 0:
                print("Weight must be greater than 0. Product was not added.")
                return
            product = PhysicalProduct(pid, name, price, stock, supplier, weight)
        else:
            download_size = float(input("Download size (MB): ").strip())
            if download_size <= 0:
                print("Download size must be greater than 0. Product was not added.")
                return
            product = DigitalProduct(pid, name, price, stock, supplier, download_size)
    except ValueError:
        print("Invalid number entered. Product was not added.")
        return

    if inventory.add_product(product):
        print("Product added successfully.")
    else:
        print(f"Product with ID {pid} already exists.")


def create_order_flow(inventory: Inventory) -> None:
    print("\nCreate an order")
    order_id = input("Order ID: ").strip()
    if not order_id:
        print("Order ID cannot be empty.")
        return
    order = Order(order_id)
    print("Enter products for this order. Leave Product ID empty to finish.")
    while True:
        pid = input("Product ID: ").strip()
        if pid == "":
            break
        product = inventory.find_product(pid)
        if product is None:
            print("Product not found.")
            continue
        try:
            quantity = int(input("Quantity: ").strip())
        except ValueError:
            print("Invalid quantity.")
            continue
        order.add_order_line(product, quantity)   # the Order creates the OrderLine
    order.display_order()


def main() -> None:
    print("--- Inventory Management System ---")
    inventory, suppliers = load_inventory()

    while True:
        show_menu()
        choice = input("Enter option: ").strip()

        if choice == "1":
            inventory.display_all()

        elif choice == "2":
            add_product_flow(inventory, suppliers)

        elif choice == "3":
            print("\nUpdate stock of a product")
            pid = input("Product ID: ").strip()
            product = inventory.find_product(pid)
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
            product = inventory.find_product(pid)
            if product is None:
                print("Product not found.")
            else:
                print("Product Found")
                product.display_information()
                print(f"    {product.get_fulfilment_info()}")
                product.get_supplier().display_information()

        elif choice == "5":
            print("\nRemove a product")
            pid = input("Enter Product ID: ").strip()
            removed = inventory.remove_product(pid)
            if removed is None:
                print("Product not found.")
            else:
                print(f"'{removed.get_name()}' was removed from the inventory.")

        elif choice == "6":
            add_supplier_flow(suppliers)

        elif choice == "7":
            display_suppliers(suppliers)

        elif choice == "8":
            create_order_flow(inventory)

        elif choice == "9":
            print("Saving inventory...")
            save_inventory(inventory, suppliers)

        elif choice == "10":
            print("Saving inventory before exit...")
            save_inventory(inventory, suppliers)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break

        else:
            print("Invalid option. Please enter 1-10.")


if __name__ == "__main__":
    main()
