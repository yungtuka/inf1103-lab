
TAX_RATE = 0.10 #tax rate on each delivery

def get_valid_input():
    stock = input("Enter the stock quantity (or type 'quit' to finish): ")
    if stock.lower() == 'quit':
        return 'quit'
    elif not stock.isdigit():
        print("Invalid input. Please enter a positive number.")
        return None
    else:
        return int(stock)



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