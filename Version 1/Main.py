# Main.py

import AddInv
import EditInv
import RemInv
import Inventory

def print_inventory(inventory):
    print("Current Inventory:")
    print(f"{'Name':<20} {'Quantity':<10} {'Category':<15} {'Price (£)'}")
    for item in inventory:
        print(f"{item[0]:<20} {item[1]:<10} {item[2]:<15} £{item[3]:.2f}")

def main():
    while True:
        print("\nInventory Management System")
        print("1. Add Item")
        print("2. Edit Item")
        print("3. Remove Item")
        print("4. View Inventory")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            name = input("Enter item name: ")
            quantity = input("Enter quantity: ")
            category = input("Enter category: ")
            price = input("Enter price (£): ")
            try:
                quantity = int(quantity)
                price = float(price)
                message = AddInv.add_item(name, quantity, category, price)
                print(message)
            except ValueError:
                print("Invalid input for quantity or price. Please enter numeric values.")

        elif choice == '2':
            index = int(input("Enter index of item to edit: "))
            new_quantity = input("Enter new quantity (leave blank to keep current): ")
            new_category = input("Enter new category (leave blank to keep current): ")
            new_price = input("Enter new price (leave blank to keep current): ")
            message = EditInv.edit_item(index, new_quantity, new_category, new_price)
            print(message)

        elif choice == '3':
            index = int(input("Enter index of item to remove: "))
            message = RemInv.remove_item(index)
            print(message)

        elif choice == '4':
            inventory = Inventory.import_inventory('inventory.db')
            print_inventory(inventory)

        elif choice == '5':
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
