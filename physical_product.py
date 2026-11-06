from product import Product
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    """A product that is stored and shipped.

    is-a Product (inheritance) + must-be-able-to be shipped (interface).
    """

    BASE_SHIPPING_FEE = 5.00   # flat fee per shipment ($)
    RATE_PER_KG = 2.50         # extra cost per kilogram ($)

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)  # reuse Product constructor
        self.__weight = weight                              # kg

    def get_weight(self):
        return self.__weight

    # Overriding: parent prints the common info, child adds its own part
    def display_information(self):
        super().display_information()
        print(f"    Weight: {self.__weight} kg")

    # Required by abstract Product
    def get_fulfilment_info(self):
        return "Physical product - requires physical shipping."

    # Required by CanBeShipped interface
    def calculate_shipping_cost(self):
        return round(self.BASE_SHIPPING_FEE + self.RATE_PER_KG * self.__weight, 2)

    # Saving / loading
    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["name"], data["price"],
                   data["stock"], data["weight"])
