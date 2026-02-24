import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import fullscreen
import dashboard  # Ensure dashboard.py has the open_dashboard function


#---------------- DATABASE PATH ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "product_stock_name.db")

conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    category_id INTEGER,
    category_name TEXT,
    company_name TEXT,
    group_name TEXT,
    sale_price REAL,
    mrp REAL,
    barcode_no TEXT,
    hsn_code TEXT
);

CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_name TEXT,
    mobile TEXT
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    mobile TEXT
);

CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS stock_in (
    stock_in_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    supplier_id INTEGER,
    quantity INTEGER,
    date TEXT
);

CREATE TABLE IF NOT EXISTS stock_out (
    stock_out_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    customer_id INTEGER,
    quantity INTEGER,
    date TEXT
);

CREATE TABLE IF NOT EXISTS purchase_bill (
    bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    bill_no TEXT,
    product_id INTEGER,
    product_name TEXT,
    date TEXT,
    payment_method TEXT,
    qty_of_product INTEGER,
    price REAL
);

CREATE TABLE IF NOT EXISTS selling_bill (
    bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    bill_no TEXT,
    product_id INTEGER,
    product_name TEXT,
    date TEXT,
    payment_method TEXT,
    qty_of_product INTEGER,
    price REAL
);

CREATE TABLE IF NOT EXISTS pending_payment_for_purchase (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bill_no TEXT,
    product_id INTEGER,
    product_name TEXT,
    date TEXT,
    payment_method TEXT,
    qty_of_product INTEGER,
    price REAL
);

CREATE TABLE IF NOT EXISTS pending_payment_for_seller (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bill_no TEXT,
    product_id INTEGER,
    product_name TEXT,
    date TEXT,
    payment_method TEXT,
    qty_of_product INTEGER,
    price REAL
);

CREATE TABLE IF NOT EXISTS shop_info (
    shop_name TEXT,
    address TEXT,
    mobile TEXT
);

CREATE TABLE IF NOT EXISTS godown_stock (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    godown_name TEXT,
    product_id INTEGER
);
""")

conn.commit()
conn.close()

# ---------------- FORGOT PASSWORD WINDOW ----------------
def open_forgot_window():
    win = tk.Toplevel(root)
    win.title("Forgot Password")
    win.geometry("700x600")
    win.configure(bg="#f4f7fe")

    # Top Blue Banner (Same as Login)
    top_banner = tk.Frame(win, bg="#5c7cfa", height=150)
    top_banner.pack(fill="x", side="top")

    # Center Card
    card = tk.Frame(win, bg="white", bd=0)
    card.place(relx=0.5, rely=0.55, anchor="center", width=400, height=500)

    # Heading
    tk.Label(card, text="Forgot Password",
             font=("Segoe UI", 22, "bold"),
             bg="white", fg="#1a1c23").pack(pady=(30, 10))

    tk.Label(card, text="Reset your account password",
             font=("Segoe UI", 10),
             bg="white", fg="#858796").pack(pady=(0, 25))

    input_container = tk.Frame(card, bg="white")
    input_container.pack(fill="both", expand=True, padx=40)

    # Username
    tk.Label(input_container, text="USERNAME",
             font=("Segoe UI", 9, "bold"),
             bg="white", fg="#5c7cfa").pack(anchor="w")

    username_entry = tk.Entry(input_container,
                              font=("Segoe UI", 11),
                              bg="#f8f9fa", fg="#333",
                              relief="flat",
                              highlightthickness=1,
                              highlightbackground="#e0e0e0",
                              highlightcolor="#5c7cfa")

    username_entry.pack(fill="x", pady=(5, 15), ipady=8)

    # New Password
    tk.Label(input_container, text="NEW PASSWORD",
             font=("Segoe UI", 9, "bold"),
             bg="white", fg="#5c7cfa").pack(anchor="w")

    new_pass_entry = tk.Entry(input_container,
                              show="•",
                              font=("Segoe UI", 11),
                              bg="#f8f9fa", fg="#333",
                              relief="flat",
                              highlightthickness=1,
                              highlightbackground="#e0e0e0",
                              highlightcolor="#5c7cfa")

    new_pass_entry.pack(fill="x", pady=(5, 15), ipady=8)

    # Confirm Password
    tk.Label(input_container, text="CONFIRM PASSWORD",
             font=("Segoe UI", 9, "bold"),
             bg="white", fg="#5c7cfa").pack(anchor="w")

    confirm_pass_entry = tk.Entry(input_container,
                                  show="•",
                                  font=("Segoe UI", 11),
                                  bg="#f8f9fa", fg="#333",
                                  relief="flat",
                                  highlightthickness=1,
                                  highlightbackground="#e0e0e0",
                                  highlightcolor="#5c7cfa")

    confirm_pass_entry.pack(fill="x", pady=(5, 25), ipady=8)

    # Reset Button
    tk.Button(input_container,
              text="RESET PASSWORD",
              bg="#5c7cfa",
              fg="black",
              font=("Segoe UI", 11, "bold"),
              relief="flat",
              cursor="heart",
              command=lambda: reset_password(
                  username_entry.get(),
                  new_pass_entry.get(),
                  confirm_pass_entry.get(),
                  win
              )).pack(fill="x", ipady=10)
    
def reset_password(username, new_password, confirm_password, window):

    if username == "" or new_password == "" or confirm_password == "":
        messagebox.showerror("Error", "All fields are required")
        return

    if new_password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()

    if user:
        cursor.execute("UPDATE users SET password=? WHERE username=?",
                       (new_password, username))
        conn.commit()
        messagebox.showinfo("Success", "Password Reset Successfully")
        window.destroy()
    else:
        messagebox.showerror("Error", "Username Not Found")

    conn.close()




# ---------------- LOGIN FUNCTION ----------------
def login():

    user = entry_user.get().strip()
    pwd = entry_pass.get().strip()


    if user == "" or pwd == "":
        messagebox.showerror("Error", "Enter username and password")
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT username, password FROM users WHERE username=? AND password=?", (user, pwd))
    result = cur.fetchone()

    conn.close()

    if result:
        messagebox.showinfo("Success", "Login Successfully")
        dashboard.open_dashboard(root)
    else:
        messagebox.showerror("Error", "Invalid username or password")


# ---------------- UI SETUP ----------------
root = tk.Tk()
root.title("Product Management System")
root.geometry("1000x700")
root.configure(bg="#f4f7fe")
fullscreen.make_fullscreen(root)


# Top blue banner
top_banner = tk.Frame(root, bg="#5c7cfa", height=250)
top_banner.pack(fill="x", side="top")

# Adaptive Card
main_frame = tk.Frame(root, bg="white", bd=0)
main_frame.place(relx=0.5, rely=0.5, anchor="center", width=450, height=580)

# Branding
tk.Label(main_frame, text="PRODUCT MANAGEMENT",
         font=("Helvetica", 12, "bold"),
         bg="white", fg="#5c7cfa").pack(pady=(40, 0))

tk.Label(main_frame, text="SYSTEM",
         font=("Helvetica", 10, "bold"),
         bg="white", fg="#adb5bd").pack(pady=(0, 25))

tk.Label(main_frame, text="Welcome Back",
         font=("Segoe UI", 28, "bold"),
         bg="white", fg="#1a1c23").pack(pady=(5, 5))

tk.Label(main_frame, text="Please login to your account",
         font=("Segoe UI", 11),
         bg="white", fg="#858796").pack(pady=(0, 40))

input_container = tk.Frame(main_frame, bg="white")
input_container.pack(fill="both", expand=True, padx=50)

# Username
tk.Label(input_container, text="USERNAME",
         font=("Segoe UI", 10, "bold"),
         bg="white", fg="#5c7cfa").pack(anchor="w")

entry_user = tk.Entry(input_container,
                      font=("Segoe UI", 12),
                      bg="#f8f9fa", fg="#333",
                      relief="flat",
                      highlightthickness=1,
                      highlightbackground="#e0e0e0",
                      highlightcolor="#5c7cfa")

entry_user.pack(fill="x", pady=(5, 20), ipady=12)

# Password
tk.Label(input_container, text="PASSWORD",
         font=("Segoe UI", 10, "bold"),
         bg="white", fg="#5c7cfa").pack(anchor="w")

entry_pass = tk.Entry(input_container,
                      show="•",
                      font=("Segoe UI", 12),
                      bg="#f8f9fa", fg="#333",
                      relief="flat",
                      highlightthickness=1,
                      highlightbackground="#e0e0e0",
                      highlightcolor="#5c7cfa")

entry_pass.pack(fill="x", pady=(5, 40), ipady=12)

# Login Button
btn_login = tk.Button(input_container,
                      text="LOGIN",
                      command=login,
                      bg="#5c7cfa",
                      fg="black",
                      font=("Segoe UI", 13, "bold"),
                      relief="flat",
                      cursor="star",
                      bd=0)

btn_login.pack(fill="x", ipady=12)

# Forgot Password Label (Clickable)
forgot_label = tk.Label(main_frame,
                        text="Forgot Password?",
                        font=("Segoe UI", 9),
                        bg="white",
                        fg="#5c7cfa",
                        cursor="spraycan")

forgot_label.pack(pady=(0, 30))
forgot_label.bind("<Button-1>", lambda e: open_forgot_window())

root.mainloop()