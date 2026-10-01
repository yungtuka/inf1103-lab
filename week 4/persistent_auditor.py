TAX_RATE = 0.10
INVENTORY_FILE = "inventory.txt"

def load_inventory(filename=INVENTORY_FILE):
    inventory = 0
    history = [] 
    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("Total="):
                    inventory = int(line.split("=", 1)[1])
                elif line.startswith("History="):
                        data = line.split("=", 1)[1]
                        history = [int(x) for x in data.split(",") if x]
    except FileNotFoundError:
        print("No saved inventory found. Starting with an empty inventory.")
    return inventory, history

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

def generate_report(total_units, failed_attempts, history):
    print("\n--- Inventory report: ---")
    print("Total Deliveries Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)
    print("Transaction history:", history)

def main():
    inventory, history = load_inventory()
    deliveries_processed = 0
    failed_entries = 0
    print(f"Loaded inventory: {inventory} units.")

    while True:
        result = get_valid_input()

        if result == 'quit':
            break
        elif result is None:
            failed_entries += 1
            continue

        # result is a valid non-negative int
        history.append(result)
        inventory = process_delivery(inventory, result)
        tax = calculate_tax(result)
        deliveries_processed += 1

        print("Current inventory:", inventory, "| Tax on this delivery:", tax)

        if inventory > 500:
            print("Warning: Inventory exceeds 500 units.")
            break

    
    generate_report(deliveries_processed, failed_entries, history)

if __name__ == "__main__":
    main()


