# Main.py

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import AddInv
import EditInv
import RemInv
import Inventory

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
            
            message = EditInv.edit_item(index, new_quantity, new_category, new_price)
            self.update_inventory_display()
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", "Please select an item to edit.")

    def update_inventory_display(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        inventory = Inventory.import_inventory('inventory.db')
        for i, (name, quantity, category, price) in enumerate(inventory):
            self.tree.insert('', 'end', iid=i, values=(name, quantity, category, price))

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
