from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier

# Maps the "type" saved in inventory.json to the class that rebuilds it.
PRODUCT_TYPES: dict[str, type[Product]] = {
    "physical": PhysicalProduct,
    "digital": DigitalProduct,
}


def create_product_from_dict(data: dict, supplier: Supplier) -> Product:
    """Build the correct Product subclass from one saved JSON entry."""
    product_type = data.get("type")
    if product_type not in PRODUCT_TYPES:
        raise ValueError(f"Unknown product type '{product_type}' for ID {data.get('id')}")
    return PRODUCT_TYPES[product_type].from_dict(data, supplier)
