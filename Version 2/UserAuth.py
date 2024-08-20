# UserAuth.py

import sqlite3
import bcrypt

def create_users_table():
    # Connect to the SQLite database
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    # Create the 'users' table if it does not already exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  # Unique identifier for each user
            username TEXT UNIQUE NOT NULL,         # Username must be unique and cannot be null
            password TEXT NOT NULL                 # Password cannot be null
        )
    ''')
    
    # Commit changes to the database
    conn.commit()
    # Close the database connection
    conn.close()

def register_user(username, password):
    # Ensure the users table exists
    create_users_table()
    
    # Connect to the SQLite database
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    # Check if the username already exists in the database
    cursor.execute('SELECT * FROM users WHERE username=?', (username,))
    if cursor.fetchone():
        conn.close()
        return "Username already exists."

    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insert the new user into the users table
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password.decode('utf-8')))
    
    # Commit changes to the database
    conn.commit()
    # Close the database connection
    conn.close()
    
    return "User registered successfully."

def authenticate_user(username, password):
    # Connect to the SQLite database
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    # Retrieve the stored password for the given username
    cursor.execute('SELECT password FROM users WHERE username=?', (username,))
    result = cursor.fetchone()
    
    # Close the database connection
    conn.close()

    # Check if a user with the provided username exists
    if result:
        stored_password = result[0]
        # Verify the provided password against the stored hashed password
        return bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8'))
    
    # Return False if the username does not exist
    return False
