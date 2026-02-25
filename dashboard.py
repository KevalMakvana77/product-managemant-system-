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
    main_container.pack(fill="both", expand=True)

    # Outer wrapper to center everything
    center_wrapper = tk.Frame(main_container, bg="#f4f7fe")
    center_wrapper.pack(expand=True)

    # --- BUTTON GRID ---
    grid_frame = tk.Frame(center_wrapper, bg="#f4f7fe")
    grid_frame.pack()

    # Make columns expandable (Perfect Center)
    for i in range(4):
        grid_frame.grid_columnconfigure(i, weight=1)

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

   