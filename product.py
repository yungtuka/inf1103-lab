from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):
    """Abstract parent for every product (SRP: one product, its own state).

    Lab 8: each Product holds a reference to its Supplier (ASSOCIATION).
    The Supplier is created elsewhere and passed in - Product does not
    create it or own it.
    """

    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier) -> None:
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        self.__supplier: Supplier = supplier   # association: a reference only

    # --- Read-only access (getters) ---
    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier

    # --- Controlled change ---
    def update_stock(self, quantity: int) -> None:
        """Set the stock to a new quantity. Negative numbers are rejected.

        Every subclass must keep this meaning (LSP).
        """
        if quantity < 0:
            print("Stock cannot be negative. Stock was not updated.")
        else:
            self.__stock = quantity
            print("Stock updated successfully.")

    def display_information(self) -> None:
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")
        print(f"    Supplier: {self.__supplier.get_name()}")

    # --- Data for saving (children add their own fields) ---
    def to_dict(self) -> dict:
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier_id": self.__supplier.get_supplier_id(),
        }

    # --- Abstract method: every child MUST implement it ---
    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Return a message describing how the product is delivered."""
        pass
