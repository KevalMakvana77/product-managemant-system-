import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import pandas as pd
from datetime import datetime
import fullscreen

def open_selling_bill_window():

    win = tk.Toplevel()
    win.title("Selling Bill Entry")
    win.configure(bg="#f4f7fe")
    fullscreen.make_fullscreen(win)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "product_stock_name.db")

    selected_rowid = 0   # ✅ FIXED

    # ================= HEADER =================
    header = tk.Frame(win, bg="#5c7cfa", height=80)
    header.pack(fill="x")

    tk.Label(header, text="SELLING BILL MANAGEMENT",
             font=("Helvetica", 18, "bold"),
             bg="#5c7cfa", fg="white").pack(pady=20)

    # ================= MAIN CARD =================
    main_frame = tk.Frame(win, bg="white", padx=25, pady=20,
                          highlightbackground="#e0e0e0",
                          highlightthickness=1)
    main_frame.place(relx=0.5, rely=0.55, anchor="center",
                     width=1200, height=630)

    # ================= LEFT FORM =================
    form_frame = tk.Frame(main_frame, bg="white")
    form_frame.pack(side="left", fill="y", padx=20)

    def load_customer_names():
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT customer_name FROM customer")
        customers = [row[0] for row in cur.fetchall()]
        conn.close()
        
        customers_name = {customer: customer for customer in customers}
        customers_names = list(customers_name.keys())

        names = ttk.Combobox(form_frame, values=customers_names,
                             font=("Segoe UI", 10),
                             state="readonly")
        names.pack(fill="x", ipady=6, pady=(0, 10))
    

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

    entry_bill_no = create_input(form_frame, "Bill No")
    entry_product_id = create_input(form_frame, "Product ID")
    entry_product_name = create_input(form_frame, "Product Name")
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
                         width=12, pady=6)

    black_btn("SAVE", lambda: save_bill()).pack(side="left", padx=5)
    black_btn("UPDATE", lambda: update_bill()).pack(side="left", padx=5)
    black_btn("DELETE", lambda: delete_bill()).pack(side="left", padx=5)
    black_btn("ANALYSIS", lambda: show_selling_analysis()).pack(side="left", padx=5)
    black_btn("GENERATE BILL", lambda: generate_bill()).pack(side="left", padx=5)

    # ================= TABLE =================
    columns = ("RowID", "Bill No", "Product ID", "Product Name",
           "Customer Name", "Date", "Payment", "Qty", "Price")
    
    tree = ttk.Treeview(right_frame, columns=columns,
                        show="headings", height=15)

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
        cur.execute("""
    SELECT bill_id,
           bill_no,
           product_id,
           product_name,
           customer_name,
           date,
           payment_method,
           qty_of_product,
           price
    FROM selling_bill
""")

        rows = cur.fetchall()
        conn.close()

        for row in rows:
            tree.insert("", tk.END, values=row)

    def select_record(event):
        nonlocal selected_rowid

        selected = tree.focus()   # ✅ FIXED
        if not selected:
            return

        row = tree.item(selected, "values")
        selected_rowid = row[0]

        fields = [entry_bill_no, entry_product_id,
          entry_product_name, entry_customer_name,
          entry_date, entry_payment,
          entry_qty, entry_price]

        for i, field in enumerate(fields):
            field.delete(0, tk.END)
            field.insert(0, row[i+1])

    def save_bill():
        data = (entry_bill_no.get(), entry_product_id.get(),
                entry_product_name.get(), entry_customer_name.get(), entry_date.get(),
                entry_payment.get(), entry_qty.get(),
                entry_price.get())

        if "" in data:
            messagebox.showerror("Error", "All fields required")
            return

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO selling_bill
            (bill_no, product_id, product_name, customer_name, date,
             payment_method, qty_of_product, price)
            VALUES (?,?,?,?,?,?,?,?)
        """, data)
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Selling Bill Saved")
        clear_fields()
        show_data()

    def update_bill():
        nonlocal selected_rowid

        if selected_rowid == 0:
            messagebox.showerror("Error", "Select bill first")
            return

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("""
    UPDATE selling_bill
    SET bill_no=?, product_id=?, product_name=?, customer_name=?, date=?,
        payment_method=?, qty_of_product=?, price=?
    WHERE bill_id=?
""", (
    entry_bill_no.get(),
    entry_product_id.get(),
    entry_product_name.get(),
    entry_customer_name.get(),
    entry_date.get(),
    entry_payment.get(),
    entry_qty.get(),
    entry_price.get(),
    selected_rowid
))

        conn.commit()
        conn.close()

        messagebox.showinfo("Updated", "Bill Updated")
        clear_fields()
        show_data()

    def delete_bill():
        nonlocal selected_rowid

        if selected_rowid == 0:
            messagebox.showerror("Error", "Select bill first")
            return

        if messagebox.askyesno("Confirm", "Delete this bill?"):
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("DELETE FROM selling_bill WHERE bill_id=?",
            (selected_rowid,))

            conn.commit()
            conn.close()

            messagebox.showinfo("Deleted", "Bill Deleted")
            clear_fields()
            show_data()

    def clear_fields():
        nonlocal selected_rowid
        selected_rowid = 0
        for field in [entry_bill_no, entry_product_id,
                      entry_product_name, entry_customer_name, entry_date,
                      entry_payment, entry_qty, entry_price]:
            field.delete(0, tk.END)
        entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

    
    def generate_bill():
        nonlocal selected_rowid

        if selected_rowid == 0:
            messagebox.showerror("Error", "Select bill first")
            return

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("""
    SELECT bill_no,
           product_id,
           product_name,
           customer_name,
           date,
           payment_method,
           qty_of_product,
           price
    FROM selling_bill
    WHERE bill_id=?
""", (selected_rowid,))
        bill = cur.fetchone()
        conn.close()

        if not bill:
            messagebox.showerror("Error", "Bill not found")
            return

        bill_no = bill[0]
        product_id = bill[1]
        product_name = bill[2]
        customer_name = bill[3]
        date = bill[4]
        payment = bill[5]
        qty = float(bill[6])
        price = float(bill[7])

        total = qty * price

        invoice = f"""
        ==============================================
                        🏪 KEVAL TRADERS
        ==============================================
        📍 Address : Rajkot, Gujarat
        📞 Mobile  : 9876543210
        🧾 GST No  : 24ABCDE1234F1Z5

        ----------------------------------------------
        SELLING INVOICE
        ----------------------------------------------

        Bill No        : {bill_no}
        Customer Name  : {customer_name}
        Date           : {date}
        Payment Method : {payment}

        ----------------------------------------------
        Product Name   : {product_name}
        Quantity       : {qty}
        Price          : ₹ {price:.2f}

        ----------------------------------------------
        TOTAL AMOUNT   : ₹ {total:.2f}
        ----------------------------------------------

        ⚠ Notice:
        If payment is not completed,
        kindly clear the bill within 5-6 days.

        🙏 Thank You for Shopping With Us!
        ==============================================
        """

        messagebox.showinfo("Selling Invoice", invoice)

    def show_selling_analysis():
            conn = sqlite3.connect(db_path)
            df = pd.read_sql_query("SELECT * FROM selling_bill", conn)
            conn.close()

            if df.empty:
                messagebox.showinfo("Info", "No selling data available")
                return

            # ---------------- Basic Calculations ----------------
            total_bills = df["bill_no"].nunique()
            total_quantity = df["qty_of_product"].sum()

            df["total_amount"] = df["qty_of_product"] * df["price"]
            total_revenue = df["total_amount"].sum()

            average_bill = total_revenue / total_bills if total_bills > 0 else 0
            average_price = df["price"].mean()
            unique_products = df["product_name"].nunique()

            # ---------------- Product Analysis ----------------
            product_summary = df.groupby("product_name")["qty_of_product"].sum()

            top_product = product_summary.idxmax()
            top_product_qty = product_summary.max()

            least_product = product_summary.idxmin()
            least_product_qty = product_summary.min()

            top5_products = product_summary.sort_values(ascending=False).head(5)

            # ---------------- Highest Bill ----------------
            bill_summary = df.groupby("bill_no")["total_amount"].sum()
            highest_bill_no = bill_summary.idxmax()
            highest_bill_amount = bill_summary.max()

            # ---------------- Payment Method ----------------
            payment_summary = df["payment_method"].value_counts()
            payment_report = "\n".join(
                [f"{method} : {count}" for method, count in payment_summary.items()]
            )
            top_payment_method = payment_summary.idxmax()

            # ---------------- Date Wise ----------------
            df["date"] = pd.to_datetime(df["date"], errors="coerce")

            date_summary = df.groupby("date")["total_amount"].sum()
            top_date = date_summary.idxmax()
            top_date_amount = date_summary.max()

            # ---------------- Monthly Summary ----------------
            df["month"] = df["date"].dt.to_period("M")
            monthly_summary = df.groupby("month")["total_amount"].sum()

            monthly_report = "\n".join(
                [f"{month} : ₹ {amount:.2f}" for month, amount in monthly_summary.items()]
            )

            top5_summary = "\n".join(
    [f"{name.strip():<25} | Qty : {qty:>5}" for name, qty in top5_products.items()]
)
            report = f"""
        ====================================
                SELLING BILL ANALYSIS
        ====================================

        💰 Total Revenue               : ₹ {total_revenue:.2f}
        🧾 Total Bills                 : {total_bills}
        📦 Total Quantity Sold         : {total_quantity}

        ------------------------------------
        📊 Average Bill Value          : ₹ {average_bill:.2f}
        💵 Average Selling Price       : ₹ {average_price:.2f}
        📦 Unique Products Sold        : {unique_products}

        ------------------------------------
        🏆 Top Selling Product
        ------------------------------------
        Product                        : {top_product}
        Quantity Sold                  : {top_product_qty}

        ------------------------------------
        🔥 Top 5 Products
        ------------------------------------
        {top5_summary}

        ------------------------------------
        💎 Highest Bill
        ------------------------------------
        Bill No                        : {highest_bill_no}
        Bill Amount                    : ₹ {highest_bill_amount:.2f}

        ------------------------------------
        💳 Payment Method Summary
        ------------------------------------
        {payment_report}

        Most Used Payment Method       : {top_payment_method}

        ------------------------------------
        📅 Highest Sales Date
        ------------------------------------
        Date                           : {top_date.date()}
        Revenue                        : ₹ {top_date_amount:.2f}

        ------------------------------------
        📆 Monthly Sales Summary
        ------------------------------------
        {monthly_report}

        ====================================
        """

            messagebox.showinfo("Selling Analysis", report)

    tree.bind("<<TreeviewSelect>>", select_record)
    show_data()
