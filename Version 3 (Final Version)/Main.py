# Main.py

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import AddInv
import EditInv
import RemInv
import Inventory
import UserAuth
import bcrypt
import sqlite3

# Create a class for entry widgets with placeholder text
class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="", **kwargs):
        # Initialize the parent class (tk.Entry)
        super().__init__(master, **kwargs)
        # Store the placeholder text
        self.placeholder = placeholder
        # Store the default foreground color of the entry widget
        self.default_fg_color = self.cget("fg")
        # Display the placeholder text
        self.put_placeholder()
        # Events to remove or display placeholder based on focus
        self.bind("<FocusIn>", self.remove_placeholder)
        self.bind("<FocusOut>", self.put_placeholder)

    def remove_placeholder(self, event):
        # Remove placeholder text when the widget gains focus
        if self.get() == self.placeholder:
            self.delete(0, tk.END)  # Clear the entry
            self.config(fg=self.default_fg_color)  # Reset foreground color

    def put_placeholder(self, event=None):
        # Display the placeholder text when the widget loses focus and the field is empty
        if not self.get():  # If entry is empty
            self.config(fg="grey")  # Set placeholder color
            self.insert(0, self.placeholder)  # Insert placeholder text
        else:
            self.config(fg=self.default_fg_color)  # Reset foreground color

# Function to display the registration window
def show_registration_window():
    # Create a new window for registration
    registration_window = tk.Toplevel()
    registration_window.title("Register")  # Set window title
    registration_window.geometry("300x200")  # Set window size
    registration_window.configure(bg="#001f3f")  # Set background color

    # Create and pack widgets for username input
    tk.Label(registration_window, text="Username", bg="#001f3f", fg="#ffffff").pack(pady=5)
    username_entry = PlaceholderEntry(registration_window, placeholder="e.g. JohnDoe")
    username_entry.pack(pady=5)

    # Create and pack widgets for password input
    tk.Label(registration_window, text="Password", bg="#001f3f", fg="#ffffff").pack(pady=5)
    password_entry = PlaceholderEntry(registration_window, placeholder="Enter password", show="*")
    password_entry.pack(pady=5)

    # Define a function for handling user registration
    def register():
        # Get input values from the entry fields
        username = username_entry.get()
        password = password_entry.get()
        # Call the register_user function from the UserAuth module
        message = UserAuth.register_user(username, password)
        # Display a message box with the registration status
        messagebox.showinfo("Register", message)
        # If registration is successful, close the window and show the login window
        if "successfully" in message:
            registration_window.destroy()
            show_login_window()

    # Create and pack the Register and Cancel buttons
    tk.Button(registration_window, text="Register", command=register, bg="#0074D9", fg="white").pack(pady=10)
    tk.Button(registration_window, text="Cancel", command=registration_window.destroy, bg="#FF4136", fg="white").pack(pady=5)

# Function to display the login window
def show_login_window():
    # Function to authenticate the user
    def authenticate_user():
        # Get input values from the entry fields
        username = entry_username.get()
        password = entry_password.get()

        # Check if both username and password are provided
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        # Connect to the SQLite database
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        # Query to fetch the password for the given username
        cursor.execute("SELECT password FROM users WHERE username=?", (username,))
        result = cursor.fetchone()
        conn.close()  # Close the database connection

        # If a user is found, check the password
        if result:
            stored_password = result[0]
            # Check if the entered password matches the stored hash
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                login_window.destroy()  # Close login window on success
                main_app()  # Launch the main application
            else:
                messagebox.showerror("Error", "Invalid username or password.")
        else:
            messagebox.showerror("Error", "User does not exist.")

    # Function to open the registration window
    def open_registration_window():
        login_window.destroy()  # Close the login window
        show_registration_window()  # Show the registration window

    # Create a new window for login
    login_window = tk.Toplevel()
    login_window.title("Login")  # Set window title
    login_window.geometry("300x200")  # Set window size
    login_window.configure(bg="#001f3f")  # Set background color

    # Create and pack widgets for username input
    tk.Label(login_window, text="Username", bg="#001f3f", fg="#ffffff").pack(pady=5)
    entry_username = PlaceholderEntry(login_window, placeholder="e.g. JohnDoe")
    entry_username.pack(pady=5)

    # Create and pack widgets for password input
    tk.Label(login_window, text="Password", bg="#001f3f", fg="#ffffff").pack(pady=5)
    entry_password = PlaceholderEntry(login_window, placeholder="Enter password", show="*")
    entry_password.pack(pady=5)

    # Create and pack the Login, Register, and Cancel buttons
    tk.Button(login_window, text="Login", command=authenticate_user, bg="#0074D9", fg="white").pack(pady=10)
    tk.Button(login_window, text="Register", command=open_registration_window, bg="#FF851B", fg="white").pack(pady=5)
    tk.Button(login_window, text="Cancel", command=login_window.destroy, bg="#FF4136", fg="white").pack(pady=5)

# Main class for the Inventory Management System
class InventoryApp:
    def __init__(self, root):
        # Initialize the main window
        self.root = root
        self.root.title("Inventory Management System")  # Set window title
        self.root.geometry("800x600")  # Set window size
        self.root.resizable(False, False)  # Prevent window resizing

        # Create a main frame within the window
        self.main_frame = tk.Frame(self.root, padx=10, pady=10, bg="#001f3f")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create and pack a title label
        self.title_label = tk.Label(self.main_frame, text="Inventory Management System", font=("Helvetica", 16, "bold"), bg="#001f3f", fg="#ffffff")
        self.title_label.pack(pady=(0, 10))

        # Create a frame for entry widgets
        self.entry_frame = tk.Frame(self.main_frame, bg="#001f3f")
        self.entry_frame.pack(pady=(0, 10))

        # Call the method to create entry widgets
        self.create_entry_widgets()

        # Create and pack an Add Item button
        self.button_add = tk.Button(self.entry_frame, text="Add Item", command=self.add_item, width=15, bg="#0074D9", fg="white")
        self.button_add.grid(row=4, column=0, columnspan=2, pady=10)

        # Create a frame for displaying the inventory
        self.display_frame = tk.Frame(self.main_frame, bg="#001f3f")
        self.display_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Create a treeview widget to display inventory items
        self.tree = ttk.Treeview(self.display_frame, columns=("Name", "Quantity", "Category", "Price"), show='headings')
        self.tree.heading("Name", text="Item Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Price", text="Price (£)")
        # Set column widths and alignment
        self.tree.column("Name", width=200, anchor='center')
        self.tree.column("Quantity", width=100, anchor='center')
        self.tree.column("Category", width=150, anchor='center')
        self.tree.column("Price", width=100, anchor='center')
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a vertical scrollbar to the treeview
        self.scrollbar = tk.Scrollbar(self.display_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.config(yscrollcommand=self.scrollbar.set)

        # Create a frame for action buttons (Edit, Remove)
        self.actions_frame = tk.Frame(self.main_frame, bg="#001f3f")
        self.actions_frame.pack(pady=(0, 10))

        # Create and pack an Edit Item button
        self.button_edit = tk.Button(self.actions_frame, text="Edit Item", command=self.edit_item, width=15, bg="#FF851B", fg="white")
        self.button_edit.grid(row=0, column=0, padx=5)

        # Create and pack a Remove Item button
        self.button_remove = tk.Button(self.actions_frame, text="Remove Item", command=self.remove_item, width=15, bg="#FF4136", fg="white")
        self.button_remove.grid(row=0, column=1, padx=5)

    # Method to create entry widgets for item details
    def create_entry_widgets(self):
        # Create and pack labels and entry widgets for item details (name, quantity, category, price)
        tk.Label(self.entry_frame, text="Item Name:", bg="#001f3f", fg="#ffffff").grid(row=0, column=0, sticky="e", pady=5)
        self.entry_name = tk.Entry(self.entry_frame, width=30)
        self.entry_name.grid(row=0, column=1, pady=5)

        tk.Label(self.entry_frame, text="Quantity:", bg="#001f3f", fg="#ffffff").grid(row=1, column=0, sticky="e", pady=5)
        self.entry_quantity = tk.Entry(self.entry_frame, width=30)
        self.entry_quantity.grid(row=1, column=1, pady=5)

        tk.Label(self.entry_frame, text="Category:", bg="#001f3f", fg="#ffffff").grid(row=2, column=0, sticky="e", pady=5)
        self.entry_category = tk.Entry(self.entry_frame, width=30)
        self.entry_category.grid(row=2, column=1, pady=5)

        tk.Label(self.entry_frame, text="Price (£):", bg="#001f3f", fg="#ffffff").grid(row=3, column=0, sticky="e", pady=5)
        self.entry_price = tk.Entry(self.entry_frame, width=30)
        self.entry_price.grid(row=3, column=1, pady=5)

    # Method to add an item to the inventory
    def add_item(self):
        # Get input values from entry widgets
        name = self.entry_name.get()
        quantity = self.entry_quantity.get()
        category = self.entry_category.get()
        price = self.entry_price.get()

        # Validate input: check if any field is empty
        if not name or not quantity or not category or not price:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            # Convert quantity and price to the appropriate types
            quantity = int(quantity)
            price = float(price)

            # Insert the item into the inventory and update the display
            Inventory.add_item(name, quantity, category, price)
            self.update_inventory_display()

            # Clear entry widgets after adding the item
            self.clear_entries()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for Quantity and Price.")

    # Method to clear entry widgets
    def clear_entries(self):
        self.entry_name.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)
        self.entry_category.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)

    # Method to update the treeview with current inventory data
    def update_inventory_display(self):
        # Clear the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch all items from the inventory and insert them into the treeview
        for item in Inventory.get_all_items():
            self.tree.insert('', tk.END, values=item)

    # Method to edit an item in the inventory
    def edit_item(self):
        # Get selected item in the treeview
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an item to edit.")
            return

        # Get item values and show a dialog to edit them
        item_values = self.tree.item(selected_item, "values")
        new_name = simpledialog.askstring("Edit Item", "Enter new item name:", initialvalue=item_values[0])
        new_quantity = simpledialog.askinteger("Edit Item", "Enter new quantity:", initialvalue=item_values[1])
        new_category = simpledialog.askstring("Edit Item", "Enter new category:", initialvalue=item_values[2])
        new_price = simpledialog.askfloat("Edit Item", "Enter new price:", initialvalue=item_values[3])

        if new_name and new_quantity and new_category and new_price:
            # Update the item in the inventory and refresh the display
            Inventory.edit_item(item_values[0], new_name, new_quantity, new_category, new_price)
            self.update_inventory_display()

    # Method to remove an item from the inventory
    def remove_item(self):
        # Get selected item in the treeview
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an item to remove.")
            return

        # Get item values and confirm deletion
        item_values = self.tree.item(selected_item, "values")
        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to remove {item_values[0]}?")
        if confirm:
            # Remove the item from the inventory and update the display
            Inventory.remove_item(item_values[0])
            self.update_inventory_display()

# Function to start the main application
def main_app():
    # Create the main application window
    root = tk.Tk()
    app = InventoryApp(root)
    app.update_inventory_display()  # Update inventory display on startup
    root.mainloop()  # Run the Tkinter event loop

# Function to create the initial login screen
def login_screen():
    # Create the root window
    root = tk.Tk()
    root.title("Inventory Management System")
    root.geometry("400x300")
    root.configure(bg="#001f3f")

    # Create and pack a title label
    tk.Label(root, text="Inventory Management System", font=("Helvetica", 16, "bold"), bg="#001f3f", fg="#ffffff").pack(pady=20)

    # Create and pack a Login button
    tk.Button(root, text="Login", command=lambda: [root.destroy(), show_login_window()], bg="#0074D9", fg="white", width=15).pack(pady=10)

    # Create and pack a Register button
    tk.Button(root, text="Register", command=lambda: [root.destroy(), show_registration_window()], bg="#FF851B", fg="white", width=15).pack(pady=10)

    # Create and pack an Exit button
    tk.Button(root, text="Exit", command=root.destroy, bg="#FF4136", fg="white", width=15).pack(pady=10)

    root.mainloop()  # Run the Tkinter event loop

# Start the application by showing the login screen
if __name__ == "__main__":
    login_screen()
