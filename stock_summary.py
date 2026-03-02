import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import fullscreen


def open_stock_summary_window():

    win = tk.Toplevel()
    win.title("Stock Summary")
    win.geometry("1000x600")
    win.configure(bg="#f4f7fe")
    fullscreen.make_fullscreen(win)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "product_stock_name.db")

    # ================= HEADER =================
    header = tk.Frame(win, bg="#5c7cfa", height=80)
    header.pack(fill="x")

    tk.Label(header,
             text="STOCK SUMMARY (IN - OUT - REMAINING)",
             font=("Helvetica", 18, "bold"),
             bg="#5c7cfa",
             fg="white").pack(pady=20)

    # ================= MAIN FRAME =================
    main_frame = tk.Frame(win, bg="white")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # ================= TREEVIEW =================
    columns = (
    "Product ID",
    "Product Name",
    "Total Stock In",
    "Total Stock Out",
    "Remaining Stock",
    "Total Purchase ₹",
    "Total Sale ₹",
    "Profit ₹"
)

    tree = ttk.Treeview(main_frame, columns=columns,
                        show="headings", height=20)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=180)

    tree.pack(fill="both", expand=True)

    # ================= LOGIC =================

    def load_stock_summary():

        for i in tree.get_children():
            tree.delete(i)

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # Get All Products
        cur.execute("SELECT product_id, product_name FROM products")
        products_data = cur.fetchall()

        for product_id, product_name in products_data:

            # ---------------- STOCK IN ----------------
            cur.execute("SELECT SUM(quantity) FROM stock_in WHERE product_id=?", (product_id,))
            total_in = cur.fetchone()[0] or 0

            # ---------------- STOCK OUT ----------------
            cur.execute("SELECT SUM(quantity) FROM stock_out WHERE product_id=?", (product_id,))
            total_out = cur.fetchone()[0] or 0

            remaining = total_in - total_out

            # ---------------- PURCHASE DATA ----------------
            cur.execute("""
                SELECT SUM(qty_of_product), SUM(qty_of_product * price)
                FROM purchase_bill
                WHERE product_id=?
            """, (product_id,))
            purchase_result = cur.fetchone()

            purchase_qty = purchase_result[0] or 0
            purchase_amount = purchase_result[1] or 0

            avg_purchase_price = purchase_amount / purchase_qty if purchase_qty > 0 else 0

            # ---------------- SELLING DATA ----------------
            cur.execute("""
                SELECT SUM(qty_of_product), SUM(qty_of_product * price)
                FROM selling_bill
                WHERE product_id=?
            """, (product_id,))
            sale_result = cur.fetchone()

            sold_qty = sale_result[0] or 0
            sale_amount = sale_result[1] or 0

            # ---------------- PROFIT CALCULATION ----------------
            cost_of_sold_goods = sold_qty * avg_purchase_price
            profit = sale_amount - cost_of_sold_goods

            # ---------------- INSERT INTO TREE ----------------
            tree.insert("", tk.END, values=(
                product_id,
                product_name,
                total_in,
                total_out,
                remaining,
                f"₹ {purchase_amount:.2f}",
                f"₹ {sale_amount:.2f}",
                f"₹ {profit:.2f}"
            ))

        conn.close()
    # ================= REFRESH BUTTON =================
    refresh_btn = tk.Button(
        win,
        text="REFRESH SUMMARY",
        bg="black",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        command=load_stock_summary
    )
    refresh_btn.pack(pady=10)

    load_stock_summary()