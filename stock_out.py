import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
from datetime import datetime
import pandas as pd
import fullscreen

def open_Stock_out_window():

    win = tk.Toplevel()
    win.title("Stock Out Management")
    win.geometry("1000x620")
    win.configure(bg="#f4f7fe")
    fullscreen.make_fullscreen(win)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "product_stock_name.db")

    selected_stock_out_id = None

    # ================= HEADER =================
    header = tk.Frame(win, bg="#5c7cfa", height=80)
    header.pack(fill="x")
    tk.Label(header, text="STOCK OUT MANAGEMENT",
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
    # -------- Customer Name Combobox --------
    tk.Label(form_frame, text="Customer Name",
            font=("Segoe UI", 10, "bold"),
            bg="white", fg="#5c7cfa").pack(anchor="w", pady=(5, 5))

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT customer_name FROM customers")
    customers = [row[0] for row in cur.fetchall()]
    conn.close()

    entry_customer_name = ttk.Combobox(form_frame,
                                    values=customers,
                                    font=("Segoe UI", 10),
                                    state="readonly")
    entry_customer_name.pack(fill="x", ipady=6, pady=(0, 10))
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

    btn_style(btn_frame, "SAVE", "#5c7cfa", lambda: add_stock_out()).pack(side="left", padx=5)
    btn_style(btn_frame, "UPDATE", "#4c6ef5", lambda: update_stock_out()).pack(side="left", padx=5)
    btn_style(btn_frame, "DELETE", "#fa5252", lambda: delete_stock_out()).pack(side="left", padx=5)
    btn_style(btn_frame, "ANALYSIS", "#fa5252", lambda: show_stock_out_analysis()).pack(side="left", padx=5)

    # ================= TABLE =================
    columns = ("ID", "Product ID", "Customer Name", "Quantity", "Date")
    tree = ttk.Treeview(right_frame, columns=columns, show="headings", height=15)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    tree.pack(fill="both", expand=True)

    # ================= LOGIC =================

    def show_data():
        for i in tree.get_children():
            tree.delete(i)

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM stock_out")
        rows = cur.fetchall()
        conn.close()

        for row in rows:
            tree.insert("", tk.END, values=row)

    def select_record(event):
        nonlocal selected_stock_out_id
        selected = tree.selection()
        if not selected:
            return

        values = tree.item(selected)['values']
        selected_stock_out_id = values[0]

        entry_product_id.delete(0, tk.END)
        entry_customer_name.delete(0, tk.END)
        entry_qty.delete(0, tk.END)
        entry_date.delete(0, tk.END)

        entry_product_id.insert(0, values[1])
        entry_customer_name.insert(0, values[2])
        entry_qty.insert(0, values[3])
        entry_date.insert(0, values[4])

    def add_stock_out():
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("""INSERT INTO stock_out (product_id, customer_name, quantity, date)
               VALUES (?,?,?,?)""",
            (entry_product_id.get(), entry_customer_name.get(),
             entry_qty.get(), entry_date.get()))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Stock Out Added")
        clear_fields()
        show_data()

    def update_stock_out():
        if not selected_stock_out_id:
            messagebox.showerror("Error", "Select record first")
            return

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("""UPDATE stock_out SET product_id=?, customer_name=?, quantity=?, date=?
               WHERE stock_out_id=?""",
            (entry_product_id.get(), entry_customer_name.get(),
             entry_qty.get(), entry_date.get(), selected_stock_out_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Updated", "Stock Out Updated")
        clear_fields()
        show_data()

    def delete_stock_out():
        if not selected_stock_out_id:
            messagebox.showerror("Error", "Select record first")
            return

        if messagebox.askyesno("Confirm", "Delete this record?"):
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("DELETE FROM stock_out WHERE stock_out_id=?", (selected_stock_out_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Deleted", "Stock Out Deleted")
            clear_fields()
            show_data()

    def clear_fields():
        nonlocal selected_stock_out_id
        selected_stock_out_id = None
        entry_product_id.delete(0, tk.END)
        entry_customer_name.delete(0, tk.END)
        entry_qty.delete(0, tk.END)
        entry_date.delete(0, tk.END)
        entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

    def show_stock_out_analysis():
        conn = sqlite3.connect(db_path)

        df = pd.read_sql_query("SELECT * FROM stock_out", conn)
        conn.close()

        if df.empty:
            messagebox.showinfo("Info", "No stock out data available")
            return

        total_records = len(df)
        total_quantity = df["quantity"].sum()

        # ---------------- Product Wise ----------------
        product_sales = df.groupby("product_id")["quantity"].sum()

        top_product = product_sales.idxmax()
        top_product_qty = product_sales.max()

        least_product = product_sales.idxmin()
        least_product_qty = product_sales.min()

        top5_products = product_sales.sort_values(ascending=False).head(5)

        # ---------------- Customer Wise ----------------
        customer_sales = df.groupby("customer_name")["quantity"].sum()

        top_customer = customer_sales.idxmax()
        top_customer_qty = customer_sales.max()

        repeat_customers = (customer_sales > 1).sum()

        # ---------------- Date Wise ----------------
        date_sales = df.groupby("date")["quantity"].sum()

        top_date = date_sales.idxmax()
        top_date_qty = date_sales.max()

        # ---------------- Monthly ----------------
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["month"] = df["date"].dt.to_period("M")

        monthly_sales = df.groupby("month")["quantity"].sum()

        monthly_summary = "\n".join(
            [f"{month} : {qty}" for month, qty in monthly_sales.items()]
        )

        top5_summary = "\n".join(
            [f"{pid} : {qty}" for pid, qty in top5_products.items()]
        )

        report = f"""
    ====================================
            STOCK OUT ANALYSIS
    ====================================

    📦 Total Records         : {total_records}
    🛒 Total Quantity Sold   : {total_quantity}

    ------------------------------------
    🏆 Top Product ID
    ------------------------------------
    Product ID               : {top_product}
    Quantity Sold            : {top_product_qty}

    ------------------------------------
    👤 Top Customer
    ------------------------------------
    Customer                 : {top_customer}
    Quantity Purchased       : {top_customer_qty}
    Repeat Customers         : {repeat_customers}

    ------------------------------------
    📅 Highest Sale Date
    ------------------------------------
    Date                     : {top_date}
    Quantity Sold            : {top_date_qty}

    ------------------------------------
    📆 Monthly Summary
    ------------------------------------
    {monthly_summary}

    ====================================
    """

        messagebox.showinfo("Stock Out Analysis", report)

    tree.bind("<<TreeviewSelect>>", select_record)
    show_data()

