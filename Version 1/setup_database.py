# Database

import sqlite3

def create_tables():
    # Connect to the SQLite database (creates the file if it does not exist)
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    # Create the 'inventory' table if it does not already exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique identifier for each item
        name TEXT NOT NULL,                    -- Name of the item
        quantity INTEGER NOT NULL,             -- Quantity of the item
        category TEXT,                         -- Category of the item
        price REAL                             -- Price of the item
    )
    ''')

    # Commit the changes to the database
    conn.commit()
    # Close the database connection
    conn.close()
    # Notify that the database setup is complete
    print("Database setup complete.")

# Run the create_tables function if this script is executed directly
if __name__ == "__main__":
    create_tables()
