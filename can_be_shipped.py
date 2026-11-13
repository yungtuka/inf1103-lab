from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """Interface-style ABC (a 'must-be-able-to' contract).

    No attributes and no implementation: any class that signs this
    contract must provide calculate_shipping_cost().
    """

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Return the shipping cost for this item."""
        pass
