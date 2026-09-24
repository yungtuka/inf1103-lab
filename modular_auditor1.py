TAX_RATE = 0.10

def get_valid_input():

    stock = input("Enter the stock quantity (or type 'quit' to finish): ")

    if stock.lower() == 'quit':
        return 'quit'
    elif not stock.isdigit():
        print("Invalid input. Please enter a positive number.")
        return None
    else:
        return int(stock)

def process_delivery(current_total, new_value):
   return current_total + new_value

def calculate_tax(amount):
    return amount * TAX_RATE

inventory = 0
failed_entries = 0

while True:
    stock = input("Enter the stock quantity (or type 'quit' to finish): ")

    if stock.lower() == 'quit':
        break

    elif not stock.isdigit():
        print("Invalid input. Please enter a positive number.")
        failed_entries += 1
        continue

    else:
        stock = int(stock)

        if stock < 0:
            print("Invalid input. Please enter a non-negative number.")
            failed_entries += 1
            continue

        inventory += stock
        print("Current inventory:", inventory)




        if inventory > 500:
            print("Warning: Inventory exceeds 500 units.")
            break

print("\n--- Inventory report: ---")
print("Total Units Processed:", inventory)
print("Number of Failed/Rejected Entries:", failed_entries)

def main():
    inventory = 0
    deliveries_processed = 0
    failed_entries = 0

    while True:
        result = get_valid_input()

        if result == 'quit':
            break
        elif result is None:
            failed_entries += 1
            continue

        # result is a valid non-negative int
        inventory = process_delivery(inventory, result)
        tax = calculate_tax(result)
        deliveries_processed += 1

        print("Current inventory:", inventory, "| Tax on this delivery:", tax)

        if inventory > 500:
            print("Warning: Inventory exceeds 500 units.")
            break

    generate_report(deliveries_processed, failed_entries)

