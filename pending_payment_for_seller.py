import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import pandas as pd
from datetime import datetime
import fullscreen

def open_pending_seller_window():

    win = tk.Toplevel()
    win.title("Pending Payment - Seller")
    win.geometry("1050x650")
    win.configure(bg="#f4f7fe")
    fullscreen.make_fullscreen(win)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "product_stock_name.db")

    selected_rowid = None

    # ================= HEADER =================
    header = tk.Frame(win, bg="#5c7cfa", height=80)
    header.pack(fill="x")

    tk.Label(header, text="PENDING SELLER PAYMENT",
             font=("Helvetica", 18, "bold"),
             bg="#5c7cfa", fg="white").pack(pady=20)

    # ================= MAIN CARD =================
    main_frame = tk.Frame(win, bg="white", padx=25, pady=20,
                          highlightbackground="#e0e0e0",
                          highlightthickness=1)
    main_frame.place(relx=0.5, rely=0.55, anchor="center",
                     width=1200, height=650)

    # ================= LEFT FORM =================
    form_frame = tk.Frame(main_frame, bg="white")
    form_frame.pack(side="left", fill="y", padx=20)

    def create_input(parent, label):
        tk.Label(parent, text=label,
                 font=("Segoe UI", 10, "bold"),
                 bg="white", fg="#5c7cfa").pack(anchor="w", pady=(5, 5))
        e = tk.Entry(parent, font=("Segoe UI", 10),
                     bg="#f8f9fa", relief="flat",
                     highlightthickness=1,
                     highlightbackground="#e0e0e0",
                     highlightcolor="#5c7cfa")
        e.pack(fill="x", ipady=6, pady=(0, 10))
        return e

    entry_purchase_bill = create_input(form_frame, "Purchase Bill Ref")
    entry_bill_no = create_input(form_frame, "Bill No")
    entry_product_id = create_input(form_frame, "Product ID")
    entry_product_name = create_input(form_frame, "Product Name")
    # -------- Supplier Name Combobox --------
    tk.Label(form_frame, text="Supplier Name",
            font=("Segoe UI", 10, "bold"),
            bg="white", fg="#5c7cfa").pack(anchor="w", pady=(5, 5))

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT supplier_name FROM suppliers")
    suppliers = [row[0] for row in cur.fetchall()]
    conn.close()

    entry_supplier_name = ttk.Combobox(form_frame,
                                    values=suppliers,
                                    font=("Segoe UI", 10),
                                    state="readonly")
    entry_supplier_name.pack(fill="x", ipady=6, pady=(0, 10))
    entry_date = create_input(form_frame, "Date")
    entry_payment = create_input(form_frame, "Payment Method")
    entry_qty = create_input(form_frame, "Quantity")
    entry_price = create_input(form_frame, "Price")

    entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

    # ================= RIGHT SIDE =================
    right_frame = tk.Frame(main_frame, bg="white")
    right_frame.pack(side="right", fill="both", expand=True, padx=20)

    btn_frame = tk.Frame(right_frame, bg="white")
    btn_frame.pack(fill="x", pady=(0, 15))

    def black_btn(text, cmd):
        return tk.Button(btn_frame, text=text, command=cmd,
                         bg="black", fg="black",
                         font=("Segoe UI", 9, "bold"),
                         relief="flat", cursor="hand2",
                         width=14, pady=6)

    black_btn("SAVE", lambda: save_entry()).pack(side="left", padx=5)
    black_btn("UPDATE", lambda: update_entry()).pack(side="left", padx=5)
    black_btn("DELETE", lambda: delete_entry()).pack(side="left", padx=5)
    black_btn("ANALYSIS", lambda: show_pending_seller_analysis()).pack(side="left", padx=5)

    # ================= TABLE =================
    columns = ("RowID", "Purchase Bill", "Bill No", "Product ID",
           "Product Name", "Supplier Name",
           "Date", "Payment", "Qty", "Price")

    tree = ttk.Treeview(right_frame, columns=columns,
                        show="headings", height=15)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=110)

    tree.pack(fill="both", expand=True)

    # ================= LOGIC =================

    def show_data():
        for i in tree.get_children():
            tree.delete(i)

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("""
    SELECT rowid,
           purchase_bill,
           bill_no,
           product_id,
           product_name,
           supplier_name,
           date,
           payment_method,
           qty_of_product,
           price
    FROM pending_payment_for_seller
""")
        rows = cur.fetchall()
        conn.close()

        for row in rows:
            tree.insert("", tk.END, values=row)

    def select_record(event):
        nonlocal selected_rowid
        selected = tree.selection()
        if not selected:
            return

        row = tree.item(selected)['values']
        selected_rowid = row[0]

        fields = [entry_purchase_bill, entry_bill_no, entry_product_id,
          entry_product_name, entry_supplier_name,
          entry_date, entry_payment,
          entry_qty, entry_price]

        for i, field in enumerate(fields):
            field.delete(0, tk.END)
            field.insert(0, row[i+1])

    def save_entry():

        data = (
            entry_purchase_bill.get(),
            entry_bill_no.get(),
            entry_product_id.get(),
            entry_product_name.get(),
            entry_supplier_name.get(),
            entry_date.get(),
            entry_payment.get(),
            entry_qty.get(),
            entry_price.get()
        )

        if "" in data:
            messagebox.showerror("Error", "All fields required")
            return

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO pending_payment_for_seller
            (purchase_bill, bill_no, product_id, product_name,
            supplier_name, date, payment_method,
            qty_of_product, price)
            VALUES (?,?,?,?,?,?,?,?,?)
        """, data)

        conn.commit()
        conn.close()

        messagebox.showinfo("Saved", "Entry Saved")
        clear_fields()
        show_data()
    def update_entry():
        if not selected_rowid:
            messagebox.showerror("Error", "Select entry first")
            return

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("""
    UPDATE pending_payment_for_seller
    SET purchase_bill=?, bill_no=?, product_id=?, product_name=?,
        supplier_name=?, date=?, payment_method=?,
        qty_of_product=?, price=?
    WHERE rowid=?
""",
(entry_purchase_bill.get(), entry_bill_no.get(),
 entry_product_id.get(), entry_product_name.get(),
 entry_supplier_name.get(),
 entry_date.get(), entry_payment.get(),
 entry_qty.get(), entry_price.get(), selected_rowid))
        conn.commit()
        conn.close()

        messagebox.showinfo("Updated", "Entry Updated")
        clear_fields()
        show_data()

    def delete_entry():
        if not selected_rowid:
            messagebox.showerror("Error", "Select entry first")
            return

        if messagebox.askyesno("Confirm", "Delete this entry?"):
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("DELETE FROM pending_payment_for_seller WHERE rowid=?", (selected_rowid,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Deleted", "Entry Deleted")
            clear_fields()
            show_data()

    def clear_fields():
        nonlocal selected_rowid
        selected_rowid = None
        for field in [entry_purchase_bill, entry_bill_no, entry_product_id,
              entry_product_name, entry_supplier_name,
              entry_date, entry_payment,
              entry_qty, entry_price]:
            field.delete(0, tk.END)
        entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

    def show_pending_seller_analysis():

        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT * FROM pending_payment_for_seller", conn)
        conn.close()

        if df.empty:
            messagebox.showinfo("Info", "No pending seller payment data available")
            return

        # ---------------- Basic Calculations ----------------
        total_bills = df["bill_no"].nunique()
        total_quantity = df["qty_of_product"].sum()

        df["total_amount"] = df["qty_of_product"].astype(float) * df["price"].astype(float)
        total_pending_amount = df["total_amount"].sum()

        average_bill = total_pending_amount / total_bills if total_bills > 0 else 0

        # ---------------- Supplier Analysis ----------------
        supplier_summary = df.groupby("supplier_name")["total_amount"].sum()

        top_supplier = supplier_summary.idxmax()
        top_supplier_amount = supplier_summary.max()

        supplier_text = ""
        for name, amount in supplier_summary.items():
            supplier_text += f"{name:<20} | ₹ {amount:.2f}\n"

        # ---------------- Product Analysis ----------------
        df["product_name"] = df["product_name"].str.strip()

        product_summary = df.groupby("product_name")["qty_of_product"].sum()

        top_product = product_summary.idxmax()
        top_product_qty = product_summary.max()

        least_product = product_summary.idxmin()
        least_product_qty = product_summary.min()

        top5_products = product_summary.sort_values(ascending=False).head(5)

        top5_summary = "\n".join(
            [f"{name:<25} | Qty : {qty:>5}" for name, qty in top5_products.items()]
        )

        # ---------------- Highest Pending Bill ----------------
        bill_summary = df.groupby("bill_no")["total_amount"].sum()
        highest_bill_no = bill_summary.idxmax()
        highest_bill_amount = bill_summary.max()

        # ---------------- Date Analysis ----------------
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

        oldest_date = df["date"].min()
        newest_date = df["date"].max()

        date_summary = df.groupby("date")["total_amount"].sum()
        top_date = date_summary.idxmax()
        top_date_amount = date_summary.max()

        # ---------------- Monthly Summary ----------------
        df["month"] = df["date"].dt.to_period("M")
        monthly_summary = df.groupby("month")["total_amount"].sum()

        monthly_report = "\n".join(
            [f"{month} : ₹ {amount:.2f}" for month, amount in monthly_summary.items()]
        )

        # ---------------- Risk Analysis ----------------
        today = pd.Timestamp.today()
        df["days_pending"] = (today - df["date"]).dt.days

        over_30 = (df["days_pending"] > 30).sum()
        over_60 = (df["days_pending"] > 60).sum()

        # ---------------- Final Report ----------------
        report = f"""
    ====================================
        PENDING SELLER PAYMENT ANALYSIS
    ====================================

    🧾 Total Pending Bills         : {total_bills}
    📦 Total Pending Quantity      : {total_quantity}
    💰 Total Pending Amount        : ₹ {total_pending_amount:.2f}
    📊 Average Bill Amount         : ₹ {average_bill:.2f}

    ------------------------------------
    🏢 Supplier Wise Pending Amount
    ------------------------------------
    {supplier_text}

    🥇 Top Supplier
    Supplier                       : {top_supplier}
    Pending Amount                 : ₹ {top_supplier_amount:.2f}

    ------------------------------------
    🏆 Most Pending Product
    ------------------------------------
    Product                        : {top_product}
    Quantity                       : {top_product_qty}

    ------------------------------------
    📉 Least Pending Product
    ------------------------------------
    Product                        : {least_product}
    Quantity                       : {least_product_qty}

    ------------------------------------
    🔥 Top 5 Pending Products
    ------------------------------------
    {top5_summary}

    ------------------------------------
    💎 Highest Pending Bill
    ------------------------------------
    Bill No                        : {highest_bill_no}
    Bill Amount                    : ₹ {highest_bill_amount:.2f}

    ------------------------------------
    📅 Date Analysis
    ------------------------------------
    Oldest Pending Date            : {oldest_date.date()}
    Newest Pending Date            : {newest_date.date()}

    Highest Pending Date           : {top_date.date()}
    Amount                         : ₹ {top_date_amount:.2f}

    ------------------------------------
    📆 Monthly Pending Summary
    ------------------------------------
    {monthly_report}

    ------------------------------------
    ⚠ Risk Analysis
    ------------------------------------
    Pending > 30 Days              : {over_30}
    Pending > 60 Days              : {over_60}

    ====================================
    """

        messagebox.showinfo("Pending Seller Analysis", report)


    tree.bind("<<TreeviewSelect>>", select_record)
    show_data()
