# AddInv.py

import Inventory

def add_item(name, quantity, category, price):
    # Convert price to float to ensure proper format
    price = float(price)
    
    # Import current inventory data from the database
    inventory = Inventory.import_inventory('inventory.db')
    
    # Append new item details to the inventory list
    inventory.append([name, quantity, category, price])
    
    # Export the updated inventory list back to the database
    Inventory.export_inventory('inventory.db', inventory)
    
    # Return a success message
    return "Item added successfully."
