import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
from src.logic.app_controller import AppController

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Guardian")
        self.root.geometry("1000x700") # Larger default size
        self.root.configure(bg="#121212") # Dark background
        
        self.controller = AppController()
        
        # UI State
        self.current_frame = None
        
        self.setup_styles()
        
        # Start Background Monitor (Global)
        from src.logic.background_monitor import BackgroundMonitor
        self.monitor = BackgroundMonitor()
        self.monitor.start()
        
        # Start with Login
        self.show_login_screen()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam') # Use a base theme that allows easier customization
        
        # Dark Theme Colors
        PRIMARY_COLOR = "#0A84FF" # Dark Mode Blue
        SECONDARY_COLOR_BG = "#1E1E1E" # Dark Surface (Cards)
        TEXT_COLOR = "#E0E0E0" # High Emphasis Text (White-ish)
        SUBTEXT_COLOR = "#A0A0A0" # Medium Emphasis Text
        BG_COLOR = "#121212" # Deep Dark Background
        INPUT_BG = "#2C2C2C" # Input Fields
        
        # Configure frames
        style.configure("TFrame", background=BG_COLOR)
        style.configure("Card.TFrame", background=SECONDARY_COLOR_BG, relief="flat", borderwidth=0)
        
        # Configure Labels
        style.configure("TLabel", background=BG_COLOR, foreground=TEXT_COLOR, font=("Segoe UI", 10))
        style.configure("Card.TLabel", background=SECONDARY_COLOR_BG, foreground=TEXT_COLOR, font=("Segoe UI", 10))
        style.configure("Header.TLabel", background=SECONDARY_COLOR_BG, foreground="#FFFFFF", font=("Segoe UI", 24, "bold"))
        style.configure("SubHeader.TLabel", background=SECONDARY_COLOR_BG, foreground=SUBTEXT_COLOR, font=("Segoe UI", 12))
        
        # Configure Buttons
        style.configure("Primary.TButton", 
                        background=PRIMARY_COLOR, 
                        foreground="white", 
                        font=("Segoe UI", 10, "bold"), 
                        borderwidth=0, 
                        focuscolor="none")
        style.map("Primary.TButton", background=[("active", "#005BB5")]) 
        
        style.configure("Secondary.TButton",
                        background="#3A3A3C", # Dark Gray Button
                        foreground=TEXT_COLOR,
                        font=("Segoe UI", 10),
                        borderwidth=0)
        style.map("Secondary.TButton", background=[("active", "#48484A")])
        
        style.configure("Danger.TButton", background="#FF453A", foreground="white", font=("Segoe UI", 10, "bold")) # Dark Mode Red
        style.map("Danger.TButton", background=[("active", "#D70015")])
        
        style.configure("Success.TButton", background="#30D158", foreground="white", font=("Segoe UI", 10, "bold")) # Dark Mode Green
        style.map("Success.TButton", background=[("active", "#248A3D")])

        # Configure Entries
        style.configure("TEntry", 
                        fieldbackground=INPUT_BG, 
                        foreground=TEXT_COLOR, 
                        insertcolor=TEXT_COLOR, # Cursor color
                        padding=5,
                        borderwidth=0)
        
        # Configure Combobox
        style.map('TCombobox', fieldbackground=[('readonly', INPUT_BG)],
                                selectbackground=[('readonly', INPUT_BG)],
                                selectforeground=[('readonly', TEXT_COLOR)],
                                foreground=[('readonly', TEXT_COLOR)])
        
        # Configure Treeview (List)
        style.configure("Treeview", 
                        background=SECONDARY_COLOR_BG,
                        fieldbackground=SECONDARY_COLOR_BG,
                        foreground=TEXT_COLOR,
                        font=("Segoe UI", 10),
                        rowheight=35,
                        borderwidth=0)
        style.configure("Treeview.Heading", 
                        background="#2C2C2C", 
                        foreground="#E0E0E0", 
                        font=("Segoe UI", 10, "bold"),
                        borderwidth=1,
                        relief="flat")
        style.map("Treeview", background=[("selected", PRIMARY_COLOR)], foreground=[("selected", "white")])

    def clear_screen(self):
        if self.current_frame:
            self.current_frame.destroy()

    def show_login_screen(self):
        self.clear_screen()
        
        # Main container to center content
        # CRITICAL FIX: Assign to self.current_frame so it can be destroyed later
        self.current_frame = ttk.Frame(self.root)
        self.current_frame.pack(expand=True, fill='both')
        
        # Card style frame for login
        card_frame = ttk.Frame(self.current_frame, style="Card.TFrame", padding="40")
        card_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Header
        ttk.Label(card_frame, text="Memory Guardian", style="Header.TLabel").pack(pady=(0, 10))
        ttk.Label(card_frame, text="Welcome Back", style="SubHeader.TLabel").pack(pady=(0, 30))
        
        # Form
        input_frame = ttk.Frame(card_frame, style="Card.TFrame")
        input_frame.pack(fill='x')
        
        ttk.Label(input_frame, text="Username", style="Card.TLabel", font=("Segoe UI", 10, "bold")).pack(anchor='w', pady=(0, 5))
        self.username_var = tk.StringVar()
        entry_user = ttk.Entry(input_frame, textvariable=self.username_var, font=("Segoe UI", 11), width=30)
        entry_user.pack(fill='x', pady=(0, 15))
        
        ttk.Label(input_frame, text="Password", style="Card.TLabel", font=("Segoe UI", 10, "bold")).pack(anchor='w', pady=(0, 5))
        self.password_var = tk.StringVar()
        entry_pass = ttk.Entry(input_frame, textvariable=self.password_var, show="*", font=("Segoe UI", 11), width=30)
        entry_pass.pack(fill='x', pady=(0, 20))
        
        # Buttons
        ttk.Button(card_frame, text="Login", style="Primary.TButton", command=self.login, cursor="hand2").pack(fill='x', pady=(0, 10), ipady=5)
        ttk.Button(card_frame, text="Create new account", style="Secondary.TButton", command=self.register, cursor="hand2").pack(fill='x', ipady=2)

    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter username and password")
            return
            
        try:
            user = self.controller.login(username, password)
            self.show_dashboard(user)
        except Exception as e:
            messagebox.showerror("Login Failed", str(e))

    def register(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter username and password")
            return
            
        try:
            user = self.controller.register(username, password)
            messagebox.showinfo("Success", f"Welcome, {user.username}!")
            self.show_dashboard(user)
        except Exception as e:
            messagebox.showerror("Registration Failed", str(e))

    def delete_account(self):
        if not messagebox.askyesno("Delete Account", "Are you sure? This will delete ALL your items and data permanently."):
            return
            
        try:
            self.controller.delete_account()
            messagebox.showinfo("Goodbye", "Account deleted successfully.")
            self.show_login_screen()
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete account: {str(e)}")

    def show_dashboard(self, user):
        self.clear_screen()
        
        # Create the MAIN dashboard container
        self.current_frame = ttk.Frame(self.root)
        self.current_frame.pack(expand=True, fill='both')

        # Top Navigation Bar
        nav_bar = ttk.Frame(self.current_frame, style="Card.TFrame", padding="15 10")
        nav_bar.pack(fill='x', side='top')
        
        ttk.Label(nav_bar, text="Memory Guardian", style="Header.TLabel", font=("Segoe UI", 14, "bold"), foreground="#007AFF").pack(side='left')
        
        user_info = ttk.Frame(nav_bar, style="Card.TFrame")
        user_info.pack(side='right')
        
        ttk.Label(user_info, text=f"{user.username}", style="Card.TLabel", font=("Segoe UI", 11, "bold")).pack(side='left', padx=15)
        ttk.Button(user_info, text="Sign Out", style="Secondary.TButton", command=self.show_login_screen, cursor="hand2").pack(side='left', padx=5)
        ttk.Button(user_info, text="Delete Account", style="Danger.TButton", command=self.delete_account, cursor="hand2").pack(side='left', padx=5)

        # Main Content Area
        main_content = ttk.Frame(self.current_frame, padding="30")
        main_content.pack(expand=True, fill='both')
        
        # -- Add Item Section (Top Card) --
        add_frame = ttk.Frame(main_content, style="Card.TFrame", padding="20")
        add_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(add_frame, text="Add New Memory Item", style="Card.TLabel", font=("Segoe UI", 12, "bold")).pack(anchor='w', pady=(0, 15))
        
        form_row = ttk.Frame(add_frame, style="Card.TFrame")
        form_row.pack(fill='x')
        
        # Name Input
        ttk.Label(form_row, text="Item Name", style="Card.TLabel", font=("Segoe UI", 9, "bold")).pack(side='left', padx=(0, 5))
        self.item_name_var = tk.StringVar()
        ttk.Entry(form_row, textvariable=self.item_name_var, width=30, font=("Segoe UI", 10)).pack(side='left', padx=(0, 20))
        
        # Category Input
        ttk.Label(form_row, text="Category", style="Card.TLabel", font=("Segoe UI", 9, "bold")).pack(side='left', padx=(0, 5))
        self.category_var = tk.StringVar()
        categories = self.controller.get_categories()
        category_names = [c.category_name for c in categories]
        self.category_cb = ttk.Combobox(form_row, textvariable=self.category_var, values=category_names, state="readonly", width=20, font=("Segoe UI", 10))
        if category_names:
            self.category_cb.current(0)
        self.category_cb.pack(side='left', padx=(0, 20))
        
        # Add Button
        ttk.Button(form_row, text="Add Item", style="Primary.TButton", command=lambda: self.add_item(categories), cursor="hand2").pack(side='left')

        # -- Items List Section (Bottom Card) --
        list_container = ttk.Frame(main_content, style="Card.TFrame", padding="20")
        list_container.pack(expand=True, fill='both') # Make this part grow
        
        list_header = ttk.Frame(list_container, style="Card.TFrame")
        list_header.pack(fill='x', pady=(0, 10), side='top')
        ttk.Label(list_header, text="My Items", style="Card.TLabel", font=("Segoe UI", 12, "bold")).pack(side='left')
        
        # Actions for Selected Item (Footer)
        # CRITICAL FIX: Pack this to the BOTTOM first so it's guaranteed space
        action_bar = ttk.Frame(list_container, style="Card.TFrame")
        action_bar.pack(fill='x', pady=(15, 0), side='bottom')
        
        # Pack buttons: Common actions LEFT, Destructive action RIGHT
        ttk.Button(action_bar, text="?  I Forgot", style="Secondary.TButton", command=self.mark_forgotten, cursor="hand2").pack(side='left')
        ttk.Frame(action_bar, style="Card.TFrame", width=10).pack(side='left') # Spacer
        ttk.Button(action_bar, text="✓  I Remembered", style="Success.TButton", command=self.mark_remembered, cursor="hand2").pack(side='left')
        ttk.Frame(action_bar, style="Card.TFrame", width=10).pack(side='left') # Spacer
        ttk.Button(action_bar, text="✎  Rename", style="Secondary.TButton", command=self.rename_item, cursor="hand2").pack(side='left')
        
        # Delete on the far right
        ttk.Button(action_bar, text="✖  Delete", style="Danger.TButton", command=self.delete_item, cursor="hand2").pack(side='right')
        
        # Treeview (Takes remaining space)
        tree_frame = ttk.Frame(list_container, style="Card.TFrame")
        tree_frame.pack(expand=True, fill='both', side='top')
        
        columns = ('name', 'category', 'status')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode='browse')
        
        self.tree.heading('name', text='Item Name', anchor='w')
        self.tree.column('name', width=250)
        
        self.tree.heading('category', text='Category', anchor='w')
        self.tree.column('category', width=150)
        
        self.tree.heading('status', text='Memory Strength', anchor='center')
        self.tree.column('status', width=100, anchor='center')
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side='left', expand=True, fill='both')
        scrollbar.pack(side='right', fill='y')

        self.refresh_items()
    def delete_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Selection", "Please select an item to delete.")
            return
        
        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this item?"):
            return

        item_id = int(selected[0])
        try:
            self.controller.delete_item(item_id)
            self.refresh_items()
            messagebox.showinfo("Success", "Item deleted.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_item(self, categories):
        name = self.item_name_var.get().strip()
        cat_name = self.category_var.get()
        
        if not name or not cat_name:
            messagebox.showwarning("Input Error", "Please provide name and category")
            return
            
        # Find category ID
        cat_id = next((c.category_id for c in categories if c.category_name == cat_name), None)
        
        if cat_id:
            try:
                self.controller.add_item(cat_id, name)
                self.item_name_var.set("")
                self.refresh_items()
                # Don't pop up success for every add, just clear the field (smoother flow)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def refresh_items(self):
        # Clear tree
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        items = self.controller.get_user_items()
        
        # Join with categories (naive implementation for display)
        categories = {c.category_id: c.category_name for c in self.controller.get_categories()}
        
        for item in items:
            cat_name = categories.get(item.category_id, "Unknown")
            status = getattr(item, 'status', 'Unknown')
            # Add basic visual indicator for status in text if needed, or just values
            self.tree.insert('', tk.END, values=(item.item_name, cat_name, status), iid=str(item.item_id))

    def mark_forgotten(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Selection", "Please select an item.")
            return
        
        item_id = int(selected[0])
        try:
            self.controller.mark_forgotten(item_id)
            self.refresh_items() # Real-time update
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def mark_remembered(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Selection", "Please select an item.")
            return
        
        item_id = int(selected[0])
        try:
            self.controller.mark_remembered(item_id)
            self.refresh_items() # Real-time update
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def rename_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Selection", "Please select an item to rename.")
            return
        
        item_id = int(selected[0])
        
        new_name = simpledialog.askstring("Rename Item", "Enter new name:")
        
        if new_name:
            try:
                self.controller.rename_item(item_id, new_name)
                self.refresh_items()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def on_close(self):
        self.controller.close()
        self.root.destroy()
