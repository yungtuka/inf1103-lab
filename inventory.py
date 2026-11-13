from product import Product


class Inventory:
    """Manages a COLLECTION of Product objects (SRP).

    Lab 8: Inventory and Product have an AGGREGATION.
    Products are created elsewhere and added here. Removing a product only
    removes the reference - the Product object itself still exists.
    The list is typed with the parent class Product, so it can hold any
    subclass (PhysicalProduct, DigitalProduct, or future ones).
    """

    def __init__(self) -> None:
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        """Add an existing Product. Returns False if the ID already exists."""
        if self.find_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> Product | None:
        """Remove the Product's reference and give the Product back.

        Returns None if no product has that ID.
        """
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)
        return product

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def display_all(self) -> None:
        print("----Current Inventory----")
        if not self.__products:
            print("The inventory is empty.")
        else:
            # Polymorphism: one loop, no type checks - each object
            # runs its own version of these methods.
            for product in self.__products:
                product.display_information()
                print(f"    {product.get_fulfilment_info()}")
        print("-------------------------")

    def get_products(self) -> list[Product]:
        return list(self.__products)   # a copy, so the real list stays private
