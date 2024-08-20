# EditInv.py

import Inventory

def edit_item(index, new_quantity, new_category, new_price):
    # Convert new_price to float if it's not None
    if new_price == "":
        new_price = None
    else:
        try:
            new_price = float(new_price)
        except ValueError:
            return "Invalid price entered."

    # Convert new_quantity to integer if it's not None
    if new_quantity == "":
        new_quantity = None
    else:
        try:
            new_quantity = int(new_quantity)
        except ValueError:
            return "Invalid quantity entered."

    # If new_category is empty, set it to None
    if new_category == "":
        new_category = None

    # Load existing inventory
    inventory = Inventory.import_inventory('inventory.db')
    
    # Ensure the provided index is within the bounds of the inventory list
    if 0 <= index < len(inventory):
        # Convert the item at the specified index from a tuple to a list for modification
        item = list(inventory[index])
        
        # Update item fields with new values if provided
        if new_quantity is not None:
            item[1] = new_quantity
        if new_category is not None:
            item[2] = new_category
        if new_price is not None:
            item[3] = new_price
        
        # Replace the old item with the updated item in the inventory list
        inventory[index] = tuple(item)
        
        # Save the updated inventory list back to the database
        Inventory.export_inventory('inventory.db', inventory)
        return "Item edited successfully."
    else:
        return "Invalid index."
