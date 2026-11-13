from product import Product
from order_line import OrderLine


class Order:
    """A customer order.

    Lab 8: Order and OrderLine have a COMPOSITION.
    The Order CREATES its own OrderLine objects inside add_order_line()
    and is the only thing that manages them. OrderLines are never passed
    in from outside or moved to another Order. When the Order goes away,
    its OrderLines go with it.
    """

    def __init__(self, order_id: str) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    def get_order_id(self) -> str:
        return self.__order_id

    def add_order_line(self, product: Product, quantity: int) -> None:
        """Create a new OrderLine for this order (composition)."""
        if quantity <= 0:
            print("Quantity must be at least 1. Order line was not added.")
            return
        order_line = OrderLine(product, quantity)   # created HERE, by the Order
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        """Remove the line for this product. Returns False if not found."""
        for order_line in self.__order_lines:
            if order_line.get_product().get_product_id() == product_id:
                self.__order_lines.remove(order_line)
                return True
        return False

    def get_order_lines(self) -> tuple[OrderLine, ...]:
        """Read-only view: callers can look, but cannot add or remove lines."""
        return tuple(self.__order_lines)

    def calculate_total(self) -> float:
        # Ask each OrderLine for its own subtotal
        return sum(line.calculate_subtotal() for line in self.__order_lines)

    def display_order(self) -> None:
        print(f"----Order {self.__order_id}----")
        if not self.__order_lines:
            print("This order has no items.")
        for order_line in self.__order_lines:
            order_line.display_information()
        print(f"Total: ${self.calculate_total():.2f}")
        print("-------------------------")
