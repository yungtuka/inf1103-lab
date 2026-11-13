"""Lab 8 tests: association, aggregation, composition, type hints, LSP
and polymorphism. Run with:  python test_lab8.py
"""
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from typing import get_type_hints

import main
from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from order_line import OrderLine


def capture(func, *args) -> str:
    """Run func and return everything it printed."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        func(*args)
    return buffer.getvalue()


# Section 6.2: works with ANY Product, never checks the subclass
def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


class TestLab8(unittest.TestCase):

    def setUp(self) -> None:
        self.supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example.com")
        self.laptop = PhysicalProduct("P001", "Laptop", 1200.0, 15, self.supplier, 2.0)
        self.windows = DigitalProduct("D001", "Windows 11 Pro", 199.0, 100, self.supplier, 5400.0)

    # ---------- Section 2: Association (Supplier - Product) ----------
    def test_2_product_stores_supplier_reference(self) -> None:
        self.assertIs(self.laptop.get_supplier(), self.supplier)
        self.assertIs(self.windows.get_supplier(), self.supplier)
        self.assertIn("Supplier: TechSource Pte Ltd", capture(self.laptop.display_information))

    def test_2_products_still_work_after_del_supplier(self) -> None:
        supplier = Supplier("S009", "Temp Supplier", "temp@example.com")
        mouse = PhysicalProduct("P002", "Mouse", 25.5, 40, supplier, 0.1)
        licence = DigitalProduct("D002", "Antivirus", 39.99, 250, supplier, 350.0)
        del supplier   # deletes the variable name, not the Supplier object
        self.assertEqual(mouse.get_supplier().get_name(), "Temp Supplier")
        self.assertEqual(licence.get_supplier().get_name(), "Temp Supplier")

    def test_2_supplier_and_product_are_separate_objects(self) -> None:
        self.assertIsNot(self.laptop, self.supplier)
        self.assertNotIsInstance(self.supplier, Product)
        self.assertIn("TechSource", capture(self.supplier.display_information))

    # ---------- Section 3: Aggregation (Inventory - Product) ----------
    def test_3_product_moves_between_inventories(self) -> None:
        inventory_a = Inventory()
        inventory_b = Inventory()
        product = self.laptop                     # created BEFORE any inventory
        inventory_a.add_product(product)
        removed = inventory_a.remove_product("P001")
        self.assertIs(removed, product)
        self.assertIsNone(inventory_a.find_product("P001"))
        self.assertEqual(product.get_name(), "Laptop")   # still usable
        inventory_b.add_product(product)
        self.assertIs(inventory_b.find_product("P001"), product)   # same object

    def test_3_emptying_inventory_does_not_destroy_products(self) -> None:
        inventory = Inventory()
        inventory.add_product(self.laptop)
        inventory.add_product(self.windows)
        inventory.remove_product("P001")
        inventory.remove_product("D001")
        self.assertEqual(inventory.get_products(), [])
        self.assertEqual(self.laptop.get_price(), 1200.0)
        self.assertEqual(self.windows.get_stock(), 100)

    def test_3_find_and_remove_missing_product_return_none(self) -> None:
        inventory = Inventory()
        self.assertIsNone(inventory.find_product("X999"))
        self.assertIsNone(inventory.remove_product("X999"))

    # ---------- Section 4: Composition (Order - OrderLine) ----------
    def test_4_order_creates_lines_and_calculates_total(self) -> None:
        order = Order("O001")
        order.add_order_line(self.laptop, 2)     # 2400.00
        order.add_order_line(self.windows, 3)    # 597.00
        lines = order.get_order_lines()
        self.assertEqual(len(lines), 2)
        self.assertIsInstance(lines[0], OrderLine)
        self.assertEqual(lines[0].calculate_subtotal(), 2400.0)
        self.assertEqual(order.calculate_total(), 2997.0)

    def test_4_same_product_in_two_orders(self) -> None:
        order_1 = Order("O001")
        order_2 = Order("O002")
        order_1.add_order_line(self.laptop, 1)
        order_2.add_order_line(self.laptop, 1)
        line_1 = order_1.get_order_lines()[0]
        line_2 = order_2.get_order_lines()[0]
        self.assertIsNot(line_1, line_2)                  # 2 OrderLine objects
        self.assertIs(line_1.get_product(), line_2.get_product())   # 1 Product

    def test_4_remove_order_line_through_order(self) -> None:
        order = Order("O001")
        order.add_order_line(self.laptop, 1)
        order.add_order_line(self.windows, 1)
        self.assertTrue(order.remove_order_line("P001"))
        self.assertEqual(len(order.get_order_lines()), 1)
        self.assertFalse(order.remove_order_line("P001"))

    def test_4_order_lines_cannot_be_changed_from_outside(self) -> None:
        order = Order("O001")
        order.add_order_line(self.laptop, 1)
        self.assertIsInstance(order.get_order_lines(), tuple)   # read-only view

    def test_4_order_line_does_not_own_product(self) -> None:
        inventory = Inventory()
        inventory.add_product(self.laptop)
        order = Order("O001")
        order.add_order_line(self.laptop, 1)
        del order                                    # the order (and its lines) go away
        self.assertIs(inventory.find_product("P001"), self.laptop)   # product remains

    # ---------- Section 5: Type hints ----------
    def test_5_type_hints_present(self) -> None:
        self.assertIs(get_type_hints(Product.__init__)["supplier"], Supplier)
        self.assertEqual(get_type_hints(Inventory.find_product)["return"], Product | None)
        self.assertEqual(get_type_hints(Inventory.remove_product)["product_id"], str)
        self.assertIs(get_type_hints(Order.add_order_line)["product"], Product)
        self.assertIs(get_type_hints(OrderLine.calculate_subtotal)["return"], float)

    # ---------- Section 6: Liskov Substitution Principle ----------
    def test_6_show_product_details_works_for_both_types(self) -> None:
        physical_output = capture(show_product_details, self.laptop)
        digital_output = capture(show_product_details, self.windows)
        self.assertIn("Weight: 2.0 kg", physical_output)
        self.assertIn("Download size: 5400.0 MB", digital_output)

    def test_6_update_stock_keeps_same_meaning(self) -> None:
        for product in [self.laptop, self.windows]:
            capture(product.update_stock, 7)
            self.assertEqual(product.get_stock(), 7)      # valid input accepted
            capture(product.update_stock, -1)
            self.assertEqual(product.get_stock(), 7)      # invalid input rejected

    # ---------- Section 7: Polymorphism ----------
    def test_7_one_loop_runs_correct_subclass_method(self) -> None:
        inventory = Inventory()
        inventory.add_product(self.laptop)
        inventory.add_product(self.windows)
        results = [product.get_fulfilment_info() for product in inventory.get_products()]
        self.assertIn("physical shipping", results[0])
        self.assertIn("download link", results[1])

    # ---------- Persistence: suppliers are shared, not copied ----------
    def test_save_and_load_keep_supplier_links(self) -> None:
        inventory = Inventory()
        inventory.add_product(self.laptop)
        inventory.add_product(self.windows)
        suppliers = {"S001": self.supplier}
        with tempfile.TemporaryDirectory() as folder:
            original_file = main.INVENTORY_FILE
            main.INVENTORY_FILE = os.path.join(folder, "test_inventory.json")
            try:
                capture(main.save_inventory, inventory, suppliers)
                buffer = io.StringIO()
                with redirect_stdout(buffer):
                    loaded, loaded_suppliers = main.load_inventory()
            finally:
                main.INVENTORY_FILE = original_file
        laptop = loaded.find_product("P001")
        windows = loaded.find_product("D001")
        self.assertIsInstance(laptop, PhysicalProduct)
        self.assertIsInstance(windows, DigitalProduct)
        self.assertIs(laptop.get_supplier(), loaded_suppliers["S001"])
        self.assertIs(laptop.get_supplier(), windows.get_supplier())   # ONE shared supplier


if __name__ == "__main__":
    unittest.main(verbosity=2)
