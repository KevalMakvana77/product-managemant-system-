import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import pandas as pd
import fullscreen

def open_product_window():
    win = tk.Toplevel()
    win.title("Product Management")
    win.geometry("1100x850")
    win.configure(bg="#f4f7fe")
    fullscreen.make_fullscreen(win)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "product_stock_name.db")
    selected_product_id = None

    header = tk.Frame(win, bg="#5c7cfa", height=80)
    header.pack(fill="x", side="top")
    tk.Label(header, text="PRODUCT INVENTORY",
             font=("Helvetica", 18, "bold"),
             bg="#5c7cfa", fg="white").pack(pady=20)

    main_frame = tk.Frame(win, bg="white", padx=25, pady=20,
                          highlightbackground="#e0e0e0",
                          highlightthickness=1)
    main_frame.place(relx=0.5, rely=0.55, anchor="center",
                     width=1200, height=650)

    form_frame = tk.Frame(main_frame, bg="white")
    form_frame.pack(side="left", fill="y", padx=15)

    def create_input(parent, label_text):
        tk.Label(parent, text=label_text,
                 font=("Segoe UI", 9, "bold"),
                 bg="white", fg="#5c7cfa").pack(anchor="w", pady=(2, 0))
        entry = tk.Entry(parent, font=("Segoe UI", 10),
                         bg="#f8f9fa", relief="flat",
                         highlightthickness=1,
                         highlightbackground="#e0e0e0",
                         highlightcolor="#5c7cfa")
        entry.pack(fill="x", pady=(0, 8), ipady=5)
        return entry

    entry_name = create_input(form_frame, "Product Name")
    entry_cat_id = create_input(form_frame, "Category ID")
    entry_cat_name = create_input(form_frame, "Category Name")
    entry_company = create_input(form_frame, "Company Name")
    entry_group = create_input(form_frame, "Group Name")
    entry_sale = create_input(form_frame, "Sale Price")
    entry_mrp = create_input(form_frame, "MRP")
    entry_barcode = create_input(form_frame, "Barcode No")
    entry_hsn = create_input(form_frame, "HSN Code")
    entry_qty = create_input(form_frame, "Quantity")

    right_frame = tk.Frame(main_frame, bg="white")
    right_frame.pack(side="right", fill="both", expand=True, padx=15)

    btn_frame = tk.Frame(right_frame, bg="white")
    btn_frame.pack(fill="x", pady=(0, 15))

    def btn_style(parent, text, color, cmd):
        return tk.Button(parent, text=text, command=cmd,
                         bg=color, fg="black",
                         font=("Segoe UI", 9, "bold"),
                         relief="flat", cursor="hand2",
                         width=14, pady=8)

    btn_style(btn_frame, "SAVE", "#5c7cfa", lambda: save_product()).pack(side="left", padx=5)
    btn_style(btn_frame, "UPDATE", "#4c6ef5", lambda: update_product()).pack(side="left", padx=5)
    btn_style(btn_frame, "DELETE", "#fa5252", lambda: delete_product()).pack(side="left", padx=5)
    btn_style(btn_frame, "ANALYSIS", "#15aabf", lambda: show_analysis()).pack(side="left", padx=5)

    # ✅ FIXED TREEVIEW
    columns = ("product_id", "product_name", "qty", "sale_price", "mrp")

    tree = ttk.Treeview(right_frame, columns=columns,
                        show="headings", height=18)

    for col in columns:
        tree.heading(col, text=col.replace("_", " ").title())
        tree.column(col, width=120)

    tree.pack(fill="both", expand=True)

    # ================= FUNCTIONS =================

    def fetch_products():
        for i in tree.get_children():
            tree.delete(i)

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("""
            SELECT product_id, product_name, qty, sale_price, mrp
            FROM products
        """)
        for row in cur.fetchall():
            tree.insert("", tk.END, values=row)
        conn.close()

    def select_product(event):
        nonlocal selected_product_id
        selected_item = tree.selection()
        if not selected_item:
            return

        values = tree.item(selected_item)['values']
        selected_product_id = values[0]

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM products WHERE product_id=?",
                    (selected_product_id,))
        row = cur.fetchone()
        conn.close()

        entries = [
            entry_name, entry_cat_id, entry_cat_name,
            entry_company, entry_group,
            entry_sale, entry_mrp,
            entry_barcode, entry_hsn,
            entry_qty  # ✅ Added qty
        ]

        for i, entry in enumerate(entries):
            entry.delete(0, tk.END)
            entry.insert(0, row[i+1])

    def save_product():
        try:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO products
                (product_name, qty, category_id, category_name,
                 company_name, group_name,
                 sale_price, mrp, barcode_no, hsn_code)
                VALUES (?,?,?,?,?,?,?,?,?,?)
            """,
            (
                entry_name.get(),
                entry_qty.get(),
                entry_cat_id.get(),
                entry_cat_name.get(),
                entry_company.get(),
                entry_group.get(),
                float(entry_sale.get() or 0),
                float(entry_mrp.get() or 0),
                entry_barcode.get(),
                entry_hsn.get()
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Product Added Successfully")
            fetch_products()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {str(e)}")

    def update_product():
        if not selected_product_id:
            return messagebox.showwarning("Select", "Please select a product")

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("""
            UPDATE products
            SET product_name=?, qty=?, category_id=?, category_name=?,
                company_name=?, group_name=?,
                sale_price=?, mrp=?, barcode_no=?, hsn_code=?
            WHERE product_id=?
        """,
        (
            entry_name.get(),
            entry_qty.get(),
            entry_cat_id.get(),
            entry_cat_name.get(),
            entry_company.get(),
            entry_group.get(),
            float(entry_sale.get() or 0),
            float(entry_mrp.get() or 0),
            entry_barcode.get(),
            entry_hsn.get(),
            selected_product_id
        ))
        conn.commit()
        conn.close()
        messagebox.showinfo("Updated", "Product Updated Successfully")
        fetch_products()

    def delete_product():
        if not selected_product_id:
            return messagebox.showwarning("Select", "Select a product")

        if messagebox.askyesno("Confirm", "Delete this product?"):
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("DELETE FROM products WHERE product_id=?",
                        (selected_product_id,))
            conn.commit()
            conn.close()
            fetch_products()

    def show_analysis():
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT * FROM products", conn)
        conn.close()

        if df.empty:
            messagebox.showinfo("Info", "No data available")
            return

        df["sale_price"] = pd.to_numeric(df["sale_price"], errors="coerce")
        df["qty"] = pd.to_numeric(df["qty"], errors="coerce")

        total_products = len(df)
        avg_price = df["sale_price"].mean()
        max_price = df["sale_price"].max()
        min_price = df["sale_price"].min()

        df["stock_value"] = df["sale_price"] * df["qty"]
        total_stock_value = df["stock_value"].sum()

        most_expensive_product = df.loc[
            df["sale_price"].idxmax(), "product_name"
        ]

        low_stock_count = len(df[df["qty"] < 5])

        report = f"""
        ====================================
                PRODUCT ANALYSIS
        ====================================

        📦 Total Products        : {total_products}

        ------------------------------------
        💰 Pricing Overview
        ------------------------------------
        Average Price            : ₹ {avg_price:.2f}
        Highest Price            : ₹ {max_price:.2f}
        Lowest Price             : ₹ {min_price:.2f}

        ------------------------------------
        📊 Inventory Overview
        ------------------------------------
        Total Stock Value        : ₹ {total_stock_value:.2f}
        Most Expensive Product   : {most_expensive_product}
        Low Stock Products (<5)  : {low_stock_count}

        ====================================
        """

        messagebox.showinfo("Product Analysis", report)

    tree.bind("<<TreeviewSelect>>", select_product)
    fetch_products()
