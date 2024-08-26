# SQL database

import sqlite3
import bcrypt

def create_tables():
    # Connect to the SQLite database (creates the file if it does not exist)
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    # Create the 'users' table if it does not already exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,   -- Unique identifier for each user
        username TEXT UNIQUE NOT NULL,          -- Username must be unique and cannot be null
        password TEXT NOT NULL                  -- Password cannot be null
    )
    ''')

    # admin123 is an example password and definitely not advisable in a real world scenario
    password = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    cursor.execute('''
    INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)
    ''', ('admin', password))

    # Commit the changes to the database
    conn.commit()
    # Close the database connection
    conn.close()
    # Notify that the database setup is complete
    print("Database setup complete.")

# Run the create_tables function if this script is executed directly
if __name__ == "__main__":
    create_tables()
