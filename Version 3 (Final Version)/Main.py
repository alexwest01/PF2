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

class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="", **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.default_fg_color = self.cget("fg")
        self.put_placeholder()
        self.bind("<FocusIn>", self.remove_placeholder)
        self.bind("<FocusOut>", self.put_placeholder)

    def remove_placeholder(self, event):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.config(fg=self.default_fg_color)

    def put_placeholder(self, event=None):
        if not self.get():
            self.config(fg="grey")
            self.insert(0, self.placeholder)
        else:
            self.config(fg=self.default_fg_color)

def show_registration_window():
    registration_window = tk.Toplevel()
    registration_window.title("Register")
    registration_window.geometry("300x200")
    registration_window.configure(bg="#001f3f")

    tk.Label(registration_window, text="Username", bg="#001f3f", fg="#ffffff").pack(pady=5)
    username_entry = PlaceholderEntry(registration_window, placeholder="e.g. JohnDoe")
    username_entry.pack(pady=5)

    tk.Label(registration_window, text="Password", bg="#001f3f", fg="#ffffff").pack(pady=5)
    password_entry = PlaceholderEntry(registration_window, placeholder="Enter password", show="*")
    password_entry.pack(pady=5)

    def register():
        username = username_entry.get()
        password = password_entry.get()
        message = UserAuth.register_user(username, password)
        messagebox.showinfo("Register", message)
        if "successfully" in message:
            registration_window.destroy()
            show_login_window()

    tk.Button(registration_window, text="Register", command=register, bg="#0074D9", fg="white").pack(pady=10)
    tk.Button(registration_window, text="Cancel", command=registration_window.destroy, bg="#FF4136", fg="white").pack(pady=5)

def show_login_window():
    def authenticate_user():
        username = entry_username.get()
        password = entry_password.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username=?", (username,))
        result = cursor.fetchone()
        conn.close()

        if result:
            stored_password = result[0]
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                login_window.destroy()
                main_app()
            else:
                messagebox.showerror("Error", "Invalid username or password.")
        else:
            messagebox.showerror("Error", "User does not exist.")

    def open_registration_window():
        login_window.destroy()
        show_registration_window()

    login_window = tk.Toplevel()
    login_window.title("Login")
    login_window.geometry("300x200")
    login_window.configure(bg="#001f3f")

    tk.Label(login_window, text="Username", bg="#001f3f", fg="#ffffff").pack(pady=5)
    entry_username = PlaceholderEntry(login_window, placeholder="e.g. JohnDoe")
    entry_username.pack(pady=5)

    tk.Label(login_window, text="Password", bg="#001f3f", fg="#ffffff").pack(pady=5)
    entry_password = PlaceholderEntry(login_window, placeholder="Enter password", show="*")
    entry_password.pack(pady=5)

    tk.Button(login_window, text="Login", command=authenticate_user, bg="#0074D9", fg="white").pack(pady=10)
    tk.Button(login_window, text="Register", command=open_registration_window, bg="#FF851B", fg="white").pack(pady=5)
    tk.Button(login_window, text="Cancel", command=login_window.destroy, bg="#FF4136", fg="white").pack(pady=5)

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        self.main_frame = tk.Frame(self.root, padx=10, pady=10, bg="#001f3f")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.title_label = tk.Label(self.main_frame, text="Inventory Management System", font=("Helvetica", 16, "bold"), bg="#001f3f", fg="#ffffff")
        self.title_label.pack(pady=(0, 10))

        self.entry_frame = tk.Frame(self.main_frame, bg="#001f3f")
        self.entry_frame.pack(pady=(0, 10))

        self.create_entry_widgets()

        self.button_add = tk.Button(self.entry_frame, text="Add Item", command=self.add_item, width=15, bg="#0074D9", fg="white")
        self.button_add.grid(row=4, column=0, columnspan=2, pady=10)

        self.display_frame = tk.Frame(self.main_frame, bg="#001f3f")
        self.display_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.tree = ttk.Treeview(self.display_frame, columns=("Name", "Quantity", "Category", "Price"), show='headings')
        self.tree.heading("Name", text="Item Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Price", text="Price (£)")
        self.tree.column("Name", width=200, anchor='center')
        self.tree.column("Quantity", width=100, anchor='center')
        self.tree.column("Category", width=150, anchor='center')
        self.tree.column("Price", width=100, anchor='center')
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.display_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.config(yscrollcommand=self.scrollbar.set)

        self.actions_frame = tk.Frame(self.main_frame, bg="#001f3f")
        self.actions_frame.pack(pady=(0, 10))

        self.button_edit = tk.Button(self.actions_frame, text="Edit Item", command=self.edit_item, width=15, bg="#FF851B", fg="white")
        self.button_edit.grid(row=0, column=0, padx=5)

        self.button_remove = tk.Button(self.actions_frame, text="Remove Item", command=self.remove_item, width=15, bg="#FF4136", fg="white")
        self.button_remove.grid(row=0, column=1, padx=5)

        self.button_logout = tk.Button(self.main_frame, text="Logout", command=self.logout, width=15, bg="#0074D9", fg="white")
        self.button_logout.pack(pady=10)

        self.update_inventory_display()

    def create_entry_widgets(self):
        self.label_name = tk.Label(self.entry_frame, text="Item Name:", bg="#001f3f", fg="#ffffff")
        self.label_name.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.entry_name = PlaceholderEntry(self.entry_frame, width=30, placeholder="e.g. Hammer")
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)
        self.entry_name.bind("<KeyPress>", self.validate_text)

        self.label_quantity = tk.Label(self.entry_frame, text="Quantity:", bg="#001f3f", fg="#ffffff")
        self.label_quantity.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.entry_quantity = PlaceholderEntry(self.entry_frame, width=30, placeholder="e.g. 10")
        self.entry_quantity.grid(row=1, column=1, padx=5, pady=5)
        self.entry_quantity.bind("<KeyPress>", self.validate_integer)

        self.label_category = tk.Label(self.entry_frame, text="Category:", bg="#001f3f", fg="#ffffff")
        self.label_category.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.entry_category = PlaceholderEntry(self.entry_frame, width=30, placeholder="e.g. Tools")
        self.entry_category.grid(row=2, column=1, padx=5, pady=5)
        self.entry_category.bind("<KeyPress>", self.validate_text)

        self.label_price = tk.Label(self.entry_frame, text="Price (£):", bg="#001f3f", fg="#ffffff")
        self.label_price.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.entry_price = PlaceholderEntry(self.entry_frame, width=30, placeholder="e.g. 4.99")
        self.entry_price.grid(row=3, column=1, padx=5, pady=5)
        self.entry_price.bind("<KeyPress>", self.validate_float)

    def validate_text(self, event):
        if event.char.isdigit():
            return "break"  # Prevent digit input

    def validate_integer(self, event):
        if not (event.char.isdigit() or event.char in '\x08\x7f'):  # Allow digits and backspace/delete
            return "break"  # Prevent non-digit input

    def validate_float(self, event):
        if not (event.char.isdigit() or event.char == '.' or event.char in '\x08\x7f'):  # Allow digits, dot, and backspace/delete
            return "break"  # Prevent non-numeric input

    def add_item(self):
        name = self.entry_name.get()
        quantity = self.entry_quantity.get()
        category = self.entry_category.get()
        price = self.entry_price.get()
        
        if not name or not category:
            messagebox.showerror("Error", "Name and Category are required.")
            return
        
        if not quantity.isdigit():
            messagebox.showerror("Error", "Quantity must be an integer.")
            return
        
        try:
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity entered.")
            return
        
        try:
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Price must be a number.")
            return
        
        message = AddInv.add_item(name, quantity, category, price)
        self.update_inventory_display()
        messagebox.showinfo("Success", message)
        
        self.clear_entries()

    def clear_entries(self):
        self.entry_name.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)
        self.entry_category.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)
        self.entry_name.put_placeholder()
        self.entry_quantity.put_placeholder()
        self.entry_category.put_placeholder()
        self.entry_price.put_placeholder()

    def remove_item(self):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            index = self.tree.index(item)
            message = RemInv.remove_item(index)
            self.update_inventory_display()
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", "Please select an item to remove.")

    def edit_item(self):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            index = self.tree.index(item)
            
            current_item = Inventory.import_inventory('inventory.db')[index]
            
            new_quantity = simpledialog.askstring("Edit Quantity", "Enter new quantity (leave blank to keep current):")
            new_category = simpledialog.askstring("Edit Category", "Enter new category (leave blank to keep current):")
            new_price = simpledialog.askstring("Edit Price", "Enter new price (leave blank to keep current):")
            
            new_quantity = self.validate_integer_value(new_quantity, current_item[1])
            if new_quantity is None:
                return
            
            new_category = new_category if new_category else current_item[2]
            
            new_price = self.validate_float_value(new_price, current_item[3])
            if new_price is None:
                return
            
            message = EditInv.edit_item(index, new_quantity, new_category, new_price)
            self.update_inventory_display()
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", "Please select an item to edit.")

    def validate_integer_value(self, value, default):
        if value == "":
            return default
        try:
            return int(value)
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity entered.")
            return None

    def validate_float_value(self, value, default):
        if value == "":
            return default
        try:
            return float(value)
        except ValueError:
            messagebox.showerror("Error", "Invalid price entered.")
            return None

    def update_inventory_display(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        inventory = Inventory.import_inventory('inventory.db')
        for item in inventory:
            item = list(item)
            try:
                item[3] = f"£{float(item[3]):.2f}"
            except ValueError:
                item[3] = "£0.00"
            self.tree.insert("", tk.END, values=item)

    def logout(self):
        self.root.destroy()
        show_login_window()

def main_app():
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    show_login_window()
    root.mainloop()
