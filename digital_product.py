from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    """A product delivered by download.

    Stock means the number of licences available, so update_stock()
    keeps exactly the same meaning as in Product (LSP).
    Does NOT implement CanBeShipped - digital products are never shipped.
    """

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, download_size: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size: float = download_size   # MB

    def get_download_size(self) -> float:
        return self.__download_size

    # Overriding: parent prints the common info, child adds its own part
    def display_information(self) -> None:
        super().display_information()
        print(f"    Download size: {self.__download_size} MB")

    # Required by abstract Product
    def get_fulfilment_info(self) -> str:
        return "Digital product - delivered via download link."

    # Saving / loading
    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data

    @classmethod
    def from_dict(cls, data: dict, supplier: Supplier) -> "DigitalProduct":
        return cls(data["id"], data["name"], data["price"],
                   data["stock"], supplier, data["download_size"])
