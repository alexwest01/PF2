# RemInv.py

import Inventory

def remove_item(index):
    # Import the current inventory from the database
    inventory = Inventory.import_inventory('inventory.db')
    
    # Check if the provided index is within the valid range
    if 0 <= index < len(inventory):
        # Remove the item at the specified index from the inventory list
        del inventory[index]
        # Save the updated inventory back to the database
        Inventory.export_inventory('inventory.db', inventory)
        return "Item removed successfully."
    else:
        return "Invalid index."
