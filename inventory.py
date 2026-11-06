class Inventory:
    """Manages a COLLECTION of Product objects (SRP)."""

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        if self.search_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def search_product(self, product_id):
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def display_all(self):
        print("----Current Inventory----")
        if not self.__products:
            print("The inventory is empty.")
        else:
            for product in self.__products:
                # Lab 7: each object runs its OWN overridden version
                product.display_information()
                print(f"    {product.get_fulfilment_info()}")
        print("-------------------------")

    def get_products(self):
        return list(self.__products)
