import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
from datetime import datetime
import pandas as pd
import fullscreen

def open_Stock_in_window():

    win = tk.Toplevel()
    win.title("Stock In Management")
    win.geometry("1000x620")
    win.configure(bg="#f4f7fe")
    fullscreen.make_fullscreen(win)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "product_stock_name.db")

    selected_stock_id = None

    # ================= HEADER =================
    header = tk.Frame(win, bg="#5c7cfa", height=80)
    header.pack(fill="x")
    tk.Label(header, text="STOCK IN MANAGEMENT",
             font=("Helvetica", 18, "bold"),
             bg="#5c7cfa", fg="white").pack(pady=20)

    # ================= MAIN CARD =================
    main_frame = tk.Frame(win, bg="white", padx=25, pady=20,
                          highlightbackground="#e0e0e0", highlightthickness=1)
    main_frame.place(relx=0.5, rely=0.55, anchor="center",
                     width=1200, height=650)

    # ================= LEFT FORM =================
    form_frame = tk.Frame(main_frame, bg="white")
    form_frame.pack(side="left", fill="y", padx=20)

    def create_input(parent, label):
        tk.Label(parent, text=label, font=("Segoe UI", 10, "bold"),
                 bg="white", fg="#5c7cfa").pack(anchor="w", pady=(5, 5))
        e = tk.Entry(parent, font=("Segoe UI", 10), bg="#f8f9fa",
                     relief="flat", highlightthickness=1,
                     highlightbackground="#e0e0e0",
                     highlightcolor="#5c7cfa")
        e.pack(fill="x", ipady=6, pady=(0, 10))
        return e

    entry_product_id = create_input(form_frame, "Product ID")
    entry_supplier_id = create_input(form_frame, "Supplier ID")
    entry_qty = create_input(form_frame, "Quantity")
    entry_date = create_input(form_frame, "Date (YYYY-MM-DD)")
    entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

    # ================= RIGHT SIDE =================
    right_frame = tk.Frame(main_frame, bg="white")
    right_frame.pack(side="right", fill="both", expand=True, padx=20)

    btn_frame = tk.Frame(right_frame, bg="white")
    btn_frame.pack(fill="x", pady=(0, 15))

    def btn_style(parent, text, color, cmd):
        return tk.Button(parent, text=text, command=cmd,
                         bg=color, fg="black",
                         font=("Segoe UI", 9, "bold"),
                         relief="flat", cursor="hand2",
                         width=12, pady=6)

    btn_style(btn_frame, "SAVE", "#5c7cfa", lambda: add_stock()).pack(side="left", padx=5)
    btn_style(btn_frame, "UPDATE", "#4c6ef5", lambda: update_stock()).pack(side="left", padx=5)
    btn_style(btn_frame, "DELETE", "#fa5252", lambda: delete_stock()).pack(side="left", padx=5)
    btn_style(btn_frame, "ANALYSIS", "#fa5252", lambda: show_stock_report()).pack(side="left", padx=5)

    # Treeview
    columns = ("ID", "Product ID", "Supplier ID", "Quantity", "Date")
    tree = ttk.Treeview(right_frame, columns=columns, show="headings", height=15)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    tree.pack(fill="both", expand=True)

    # ================= LOGIC =================

    def show_stock():
        for i in tree.get_children():
            tree.delete(i)

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM stock_in")
        rows = cur.fetchall()
        conn.close()

        for row in rows:
            tree.insert("", tk.END, values=row)

    def select_stock(event):
        nonlocal selected_stock_id
        selected = tree.selection()
        if not selected:
            return

        values = tree.item(selected)['values']
        selected_stock_id = values[0]

        entry_product_id.delete(0, tk.END)
        entry_supplier_id.delete(0, tk.END)
        entry_qty.delete(0, tk.END)
        entry_date.delete(0, tk.END)

        entry_product_id.insert(0, values[1])
        entry_supplier_id.insert(0, values[2])
        entry_qty.insert(0, values[3])
        entry_date.insert(0, values[4])

    def add_stock():
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("""INSERT INTO stock_in (product_id, supplier_id, quantity, date)
                       VALUES (?,?,?,?)""",
                    (entry_product_id.get(), entry_supplier_id.get(),
                     entry_qty.get(), entry_date.get()))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Stock Added")
        clear_fields()
        show_stock()

    def update_stock():
        if not selected_stock_id:
            messagebox.showerror("Error", "Select record first")
            return

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("""UPDATE stock_in SET product_id=?, supplier_id=?, quantity=?, date=?
                       WHERE stock_in_id=?""",
                    (entry_product_id.get(), entry_supplier_id.get(),
                     entry_qty.get(), entry_date.get(), selected_stock_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Updated", "Stock Updated")
        clear_fields()
        show_stock()

    def delete_stock():
        if not selected_stock_id:
            messagebox.showerror("Error", "Select record first")
            return

        if messagebox.askyesno("Confirm", "Delete this record?"):
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("DELETE FROM stock_in WHERE stock_in_id=?", (selected_stock_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Deleted", "Stock Deleted")
            clear_fields()
            show_stock()

    def clear_fields():
        nonlocal selected_stock_id
        selected_stock_id = None
        entry_product_id.delete(0, tk.END)
        entry_supplier_id.delete(0, tk.END)
        entry_qty.delete(0, tk.END)
        entry_date.delete(0, tk.END)
        entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

    def show_stock_report():

        conn = sqlite3.connect(db_path)

        # Database mathi stock_in data lao
        df = pd.read_sql_query("SELECT * FROM stock_in", conn)

        if df.empty:
            messagebox.showinfo("Stock Report", "No stock data found!")
            return

        # 🔹 Total Stock Quantity
        total_stock = df["quantity"].sum()

        # 🔹 Product ID wise total stock
        product_summary = df.groupby("product_id")["quantity"].sum()

        # 🔹 Date wise total stock
        date_summary = df.groupby("date")["quantity"].sum()

        # 🔹 Highest stock product
        highest_product = product_summary.idxmax()
        highest_quantity = product_summary.max()

       # Product summary ne proper format ma convert karo
        product_text = ""
        for pid, qty in product_summary.items():
            product_text += f"Product ID {pid}  →  {qty}\n"

        # Date summary ne proper format ma convert karo
        date_text = ""
        for d, qty in date_summary.items():
            date_text += f"{d}  →  {qty}\n"


        report = f"""
        ====================================
                    STOCK REPORT
        ====================================

        📦 Total Stock Quantity : {total_stock}

        🏆 Highest Stock Product ID : {highest_product}
        Quantity : {highest_quantity}

        ------------------------------------
        📊 Stock Per Product ID:
        {product_text}

        ------------------------------------
        📅 Stock Per Date:
        {date_text}
        """


        messagebox.showinfo("Stock Report", report)

    tree.bind("<<TreeviewSelect>>", select_stock)
    show_stock()
