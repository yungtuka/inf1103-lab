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

def generate_report(total_units, failed_attempts):
    print("\n--- Inventory report: ---")
    print("Total Deliveries Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)

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

if __name__ == "__main__":
    main()


