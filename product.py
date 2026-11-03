class Product:
    """Represents ONE product and manages its own state (SRP)."""

    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    # --- Read-only access (getters) ---
    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    # --- Controlled change ---
    def update_stock(self, quantity):
        if quantity < 0:
            print("Stock cannot be negative. Stock was not updated.")
        else:
            self.__stock = quantity
            print("Stock updated successfully.")

    def display_information(self):
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")
