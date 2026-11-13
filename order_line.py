from product import Product


class OrderLine:
    """One product and the quantity ordered, inside ONE Order.

    Lab 8: OrderLine is the PART in a COMPOSITION with Order.
    Only Order creates OrderLine objects.
    OrderLine refers to a Product (association) but does not own it.
    """

    def __init__(self, product: Product, quantity: int) -> None:
        self.__product: Product = product
        self.__quantity: int = quantity

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity

    def display_information(self) -> None:
        print(f"{self.__product.get_name()} x {self.__quantity} "
              f"@ ${self.__product.get_price():.2f} = ${self.calculate_subtotal():.2f}")
