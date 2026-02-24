import tkinter as tk
from tkinter import ttk
import pandas as pd
import sqlite3
import customer, products, purchase_bill, stock_in, stock_out
import suppliers, godown_stock, shop_info
import pending_payment_for_purchase, pending_payment_for_seller
import selling_bill, categories
import fullscreen
import os

def open_dashboard(root):
    root.withdraw()

    dash = tk.Toplevel(root)
    dash.title("Product Management System - Dashboard")
    dash.geometry("1100x750")
    fullscreen.make_fullscreen(dash)
    dash.configure(bg="#f4f7fe")

    # --- TOP HEADER ---
    header = tk.Frame(dash, bg="#5c7cfa", height=120)
    header.pack(fill="x", side="top")

    tk.Label(header, text="PRODUCT MANAGEMENT SYSTEM",
             bg="#5c7cfa", fg="white",
             font=("Helvetica", 18, "bold")).pack(pady=(25, 0))

    tk.Label(header, text="Admin Control Panel",
             bg="#5c7cfa", fg="#dcebff",
             font=("Segoe UI", 10)).pack()

    # --- BUTTON STYLING ---
    style = ttk.Style()
    style.theme_use("clam")

    style.configure("DashCard.TButton",
                    font=("Segoe UI", 11, "bold"),
                    background="white",
                    foreground="#5c7cfa",
                    padding=20,
                    borderwidth=0)

    style.map("DashCard.TButton",
              background=[("active", "#5c7cfa")],
              foreground=[("active", "white")])

    # --- MAIN CONTAINER ---
    main_container = tk.Frame(dash, bg="#f4f7fe")
    main_container.pack(fill="both", expand=True, padx=40, pady=40)

    # --- BUTTON GRID ---
    grid_frame = tk.Frame(main_container, bg="#f4f7fe")
    grid_frame.pack()

    buttons = [
        ("📂 Categories", categories.open_categories_window),
        ("📦 Products", products.open_product_window),
        ("👥 Customers", customer.open_customer_window),
        ("🚚 Suppliers", suppliers.open_open_Suppliers_window),
        ("📥 Stock In", stock_in.open_Stock_in_window),
        ("📤 Stock Out", stock_out.open_Stock_out_window),
        ("🧾 Purchase Bill", purchase_bill.open_Purchase_bill_window),
        ("💰 Selling Bill", selling_bill.open_selling_bill_window),
        ("⌛ Unpaid Suppliers", pending_payment_for_seller.open_pending_seller_window),
        ("⏳ Unpaid Customers", pending_payment_for_purchase.open_pending_purchase_window),
        ("🏪 Shop Info", shop_info.open_shop_info_window),
        ("🏬 Godown Stock", godown_stock.open_godown_stock_window)
    ]

    row, col = 0, 0
    for text, cmd in buttons:
        card_border = tk.Frame(grid_frame,
                               bg="white",
                               highlightbackground="#e0e0e0",
                               highlightthickness=1)
        card_border.grid(row=row, column=col, padx=15, pady=15)

        btn = ttk.Button(card_border,
                         text=text,
                         style="DashCard.TButton",
                         command=cmd,
                         width=25)
        btn.pack(ipady=10)

        col += 1
        if col == 4:
            col = 0
            row += 1

    # ================= SUMMARY SECTION (NOW CORRECT PLACE) =================
    summary_frame = tk.Frame(main_container, bg="#f4f7fe")
    summary_frame.pack(pady=40)

    def load_dashboard_summary():

        # 🔥 Clear previous summary
        for widget in summary_frame.winfo_children():
            widget.destroy()

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "product_stock_name.db")

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        cur.execute("SELECT SUM(qty_of_product * price) FROM selling_bill")
        total_revenue = cur.fetchone()[0] or 0

        cur.execute("SELECT COUNT(DISTINCT bill_no) FROM selling_bill")
        total_bills = cur.fetchone()[0] or 0

        cur.execute("SELECT SUM(qty_of_product) FROM selling_bill")
        total_qty_sold = cur.fetchone()[0] or 0

        avg_bill = total_revenue / total_bills if total_bills > 0 else 0

        cur.execute("SELECT SUM(qty_of_product * price) FROM purchase_bill")
        total_purchase = cur.fetchone()[0] or 0

        conn.close()

        stats = [
            ("💰 Revenue", f"₹ {total_revenue:.2f}"),
            ("🧾 Bills", f"{total_bills}"),
            ("📦 Sold Qty", f"{total_qty_sold}"),
            ("📊 Avg Bill", f"₹ {avg_bill:.2f}"),
            ("💸 Purchase", f"₹ {total_purchase:.2f}")
        ]

        # Single Outer Frame (Table Border)
        table_frame = tk.Frame(summary_frame,
                            bg="white",
                            highlightbackground="#d0d0d0",
                            highlightthickness=1)

        table_frame.pack(pady=30)

        # First Row (Titles)
        for col, (title, value) in enumerate(stats):

            title_label = tk.Label(table_frame,
                                text=title,
                                font=("Segoe UI", 10, "bold"),
                                bg="white",
                                fg="#5c7cfa",
                                padx=25, pady=10,
                                borderwidth=1,
                                relief="solid")

            title_label.grid(row=0, column=col, sticky="nsew")

        # Second Row (Values)
        for col, (title, value) in enumerate(stats):

            value_label = tk.Label(table_frame,
                                text=value,
                                font=("Segoe UI", 14, "bold"),
                                bg="white",
                                fg="black",
                                padx=25, pady=15,
                                borderwidth=1,
                                relief="solid")

            value_label.grid(row=1, column=col, sticky="nsew")

        # Equal column width
        for i in range(len(stats)):
            table_frame.grid_columnconfigure(i, weight=1)

    load_dashboard_summary()

    # --- Logout ---
    def logout():
        dash.destroy()
        root.deiconify()

    btn_logout = tk.Button(dash, text="LOGOUT",
                           command=logout,
                           bg="#fa5252", fg="black",
                           font=("Segoe UI", 10, "bold"),
                           relief="flat", cursor="pirate",
                           padx=30, pady=10)

    btn_logout.pack(side="bottom", pady=30)

    refresh_btn = tk.Button(main_container,
                        text="🔄 Refresh",
                        command=load_dashboard_summary,
                        bg="white",                 # ✅ White background
                        fg="#5c7cfa",               # ✅ Blue text
                        font=("Segoe UI", 10, "bold"),
                        relief="flat",              # ✅ Remove 3D look
                        highlightbackground="#e0e0e0",
                        highlightthickness=1,      # ✅ Light border
                        bd=0,
                        padx=25,
                        pady=5,
                        cursor="hand2")

    refresh_btn.pack(pady=5)

    dash.protocol("WM_DELETE_WINDOW", root.destroy)