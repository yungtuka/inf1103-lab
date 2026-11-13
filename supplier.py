class Supplier:
    """Represents a company that supplies products.

    Lab 8: Supplier and Product have an ASSOCIATION.
    A supplier is not part of a product and a product is not part of a
    supplier - they simply know about each other and both can exist alone.
    """

    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        self.__supplier_id: str = supplier_id
        self.__name: str = name
        self.__contact_email: str = contact_email

    # --- Read-only access (getters) ---
    def get_supplier_id(self) -> str:
        return self.__supplier_id

    def get_name(self) -> str:
        return self.__name

    def get_contact_email(self) -> str:
        return self.__contact_email

    def display_information(self) -> None:
        print(f"Supplier: {self.__name} (ID: {self.__supplier_id}) | "
              f"Email: {self.__contact_email}")

    # --- Saving / loading ---
    def to_dict(self) -> dict:
        return {
            "supplier_id": self.__supplier_id,
            "name": self.__name,
            "contact_email": self.__contact_email,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Supplier":
        return cls(data["supplier_id"], data["name"], data["contact_email"])
