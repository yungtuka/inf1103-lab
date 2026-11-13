from product import Product
from can_be_shipped import CanBeShipped
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):
    """A product that is stored and shipped.

    is-a Product (inheritance) + must-be-able-to be shipped (interface).
    """

    BASE_SHIPPING_FEE: float = 5.00   # flat fee per shipment ($)
    RATE_PER_KG: float = 2.50         # extra cost per kilogram ($)

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, weight: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight: float = weight   # kg

    def get_weight(self) -> float:
        return self.__weight

    # Overriding: parent prints the common info, child adds its own part
    def display_information(self) -> None:
        super().display_information()
        print(f"    Weight: {self.__weight} kg")

    # Required by abstract Product
    def get_fulfilment_info(self) -> str:
        return (f"Physical product - requires physical shipping "
                f"(shipping cost: ${self.calculate_shipping_cost():.2f}).")

    # Required by CanBeShipped interface
    def calculate_shipping_cost(self) -> float:
        return round(self.BASE_SHIPPING_FEE + self.RATE_PER_KG * self.__weight, 2)

    # Saving / loading
    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data

    @classmethod
    def from_dict(cls, data: dict, supplier: Supplier) -> "PhysicalProduct":
        return cls(data["id"], data["name"], data["price"],
                   data["stock"], supplier, data["weight"])
