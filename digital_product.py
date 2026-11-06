from product import Product


class DigitalProduct(Product):
    """A product delivered by download.

    Does NOT implement CanBeShipped - digital products are never shipped.
    """

    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)  # reuse Product constructor
        self.__download_size = download_size                # MB

    def get_download_size(self):
        return self.__download_size

    # Overriding: parent prints the common info, child adds its own part
    def display_information(self):
        super().display_information()
        print(f"    Download size: {self.__download_size} MB")

    # Required by abstract Product
    def get_fulfilment_info(self):
        return "Digital product - delivered via download link."

    # Saving / loading
    def to_dict(self):
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["name"], data["price"],
                   data["stock"], data["download_size"])
