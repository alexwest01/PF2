# Inventory.py

import sqlite3
import logging

# Configure logging to capture errors and important information
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def import_inventory(file_name):
    # Initialize an empty list to hold inventory data
    inventory = []
    
    try:
        # Use context manager to handle the database connection
        with sqlite3.connect(file_name) as conn:
            cursor = conn.cursor()
            # Execute SQL query to fetch inventory data
            cursor.execute("SELECT name, quantity, category, price FROM inventory")
            # Fetch all rows from the executed query
            inventory = cursor.fetchall()
    
    except sqlite3.Error as e:
        # Log any errors encountered during the process
        logging.error(f"Error importing inventory: {e}")
    
    # Return the fetched inventory data
    return inventory

def export_inventory(file_name, inventory):
    try:
        # Use context manager to handle the database connection
        with sqlite3.connect(file_name) as conn:
            cursor = conn.cursor()
            
            # Create the inventory table if it does not exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS inventory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    name TEXT, 
                    quantity INTEGER, 
                    category TEXT, 
                    price REAL
                )
            """)
            
            # Remove all existing data from the inventory table
            cursor.execute("DELETE FROM inventory")
            
            # Insert new inventory data into the table
            cursor.executemany("INSERT INTO inventory (name, quantity, category, price) VALUES (?, ?, ?, ?)", inventory)
            
            # Commit the transaction to save changes
            conn.commit()
            
            # Log success message
            logging.info("Inventory exported successfully.")
    
    except sqlite3.Error as e:
        # Log any errors encountered during the process
        logging.error(f"Error exporting inventory: {e}")
