import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import pandas as pd
from datetime import datetime
import fullscreen
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import numpy as np

def open_pending_purchase_window():

    win = tk.Toplevel()
    win.title("Pending Payment - Buyer")
    win.geometry("1050x650")
    win.configure(bg="#f4f7fe")
    fullscreen.make_fullscreen(win)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "product_stock_name.db")

    selected_rowid = None

    # ---------- AI Chat Training ----------

    training_questions = [

        "how many pending",
        "total pending",
        "count pending",
        "number of pending",

        "show pending",
        "list pending",
        "show all pending",
        "pending list",

        "total amount",
        "pending amount",
        "total pending amount",
        "how much pending",

        "total qty",
        "total quantity",
        "pending qty",

        "top customer",
        "highest customer",
        "max customer",

        "top product",
        "highest product",
        "most product",

        "highest bill",
        "max bill",
        "big bill",

        "lowest bill",
        "small bill",

        "average bill",
        "average amount",

        "today pending",
        "today data",

        "payment pending",
        "pending payment",

        "over 30 days",
        "old pending",

        "customer list",
        "product list"

    ]


    training_labels = [

        "count",
        "count",
        "count",
        "count",

        "list",
        "list",
        "list",
        "list",

        "amount",
        "amount",
        "amount",
        "amount",

        "qty",
        "qty",
        "qty",

        "customer",
        "customer",
        "customer",

        "product",
        "product",
        "product",

        "highbill",
        "highbill",
        "highbill",

        "lowbill",
        "lowbill",

        "average",
        "average",

        "today",
        "today",

        "payment",
        "payment",

        "old",
        "old",

        "customerlist",
        "productlist"

    ]

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(training_questions)

    model = LogisticRegression()
    model.fit(X, training_labels)

    # ================= HEADER =================
    header = tk.Frame(win, bg="#5c7cfa", height=80)
    header.pack(fill="x")

    tk.Label(
        header,
        text="PENDING BUYER PAYMENT",
        font=("Helvetica", 18, "bold"),
        bg="#5c7cfa",
        fg="white"
    ).pack(pady=20)

    # ================= MAIN CARD =================
    main_frame = tk.Frame(
        win,
        bg="white",
        padx=25,
        pady=20,
        highlightbackground="#e0e0e0",
        highlightthickness=1
    )

    main_frame.place(
        relx=0.5,
        rely=0.55,
        anchor="center",
        width=1200,
        height=700
    )

    # ================= LEFT FORM =================
    form_frame = tk.Frame(main_frame, bg="white")
    form_frame.pack(side="left", fill="y", padx=20)

    def create_input(parent, label):
        tk.Label(
            parent,
            text=label,
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#5c7cfa"
        ).pack(anchor="w", pady=(5, 5))

        e = tk.Entry(
            parent,
            font=("Segoe UI", 10),
            bg="#f8f9fa",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#e0e0e0",
            highlightcolor="#5c7cfa"
        )
        e.pack(fill="x", ipady=6, pady=(0, 10))
        return e

    entry_purchase_bill = create_input(form_frame, "Purchase Bill Ref")
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
     # -------- Payment Method Combobox --------
    tk.Label(form_frame, text="Payment Method",
            font=("Segoe UI", 10, "bold"),
            bg="white", fg="#5c7cfa").pack(anchor="w", pady=(5, 5))

    payment_methods = ["Cash", "UPI", "Card", "Net Banking", "Cheque", "Pending"]

    entry_payment = ttk.Combobox(
        form_frame,
        values=payment_methods,
        font=("Segoe UI", 10),
        state="readonly"
    )
    entry_payment.pack(fill="x", ipady=6, pady=(0, 10))
    entry_qty = create_input(form_frame, "Quantity")
    entry_price = create_input(form_frame, "Price")

    entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

    # ================= RIGHT SIDE =================
    right_frame = tk.Frame(main_frame, bg="white")
    right_frame.pack(side="right", fill="both", expand=True, padx=20)

    btn_frame = tk.Frame(right_frame, bg="white")
    btn_frame.pack(fill="x", pady=(0, 15))

    def black_btn(parent, text, color, cmd):
        return tk.Button(
            parent,
            text=text,
            command=cmd,
            bg=color,
            fg="black",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            cursor="hand2",
            width=12,
            pady=6
        )


    black_btn(btn_frame, "SAVE", "#5c7cfa",
            lambda: save_entry()).pack(side="left", padx=5)

    black_btn(btn_frame, "UPDATE", "#20c997",
            lambda: update_entry()).pack(side="left", padx=5)

    black_btn(btn_frame, "DELETE", "#fa5252",
            lambda: delete_entry()).pack(side="left", padx=5)

    black_btn(btn_frame, "ANALYSIS", "#845ef7",
            lambda: show_pending_buyer_analysis()).pack(side="left", padx=5)

    black_btn(btn_frame, "LOGOUT", "#000000",
            lambda: win.destroy()).pack(side="right", padx=5)

    # ================= TABLE =================
    columns = (
    "RowID",
    "Purchase Bill",
    "Bill No",
    "Product ID",
    "Product Name",
    "Customer Name",
    "Date",
    "Payment",
    "Qty",
    "Price"
)

    tree = ttk.Treeview(
        right_frame,
        columns=columns,
        show="headings",
        height=15
    )

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=110)

    tree.pack(fill="both", expand=True)

    # ================= CHATBOT =================

    chat_frame = tk.Frame(
        right_frame,
        bg="white",
        padx=10,
        pady=10,
        highlightbackground="#e0e0e0",
        highlightthickness=1
    )
    chat_frame.pack(fill="x", pady=10)

    tk.Label(
        chat_frame,
        text="AI Chatbot",
        font=("Segoe UI", 10, "bold"),
        bg="white",
        fg="#5c7cfa"
    ).pack(anchor="w", pady=(0,5))


    chat_display = tk.Listbox(
        chat_frame,
        height=6,
        bg="#f8f9fa",
        font=("Segoe UI", 9),
        relief="flat",
        highlightthickness=1,
        highlightbackground="#e0e0e0"
    )
    chat_display.pack(fill="x", padx=5, pady=5)


    chat_entry = tk.Entry(
        chat_frame,
        font=("Segoe UI", 10),
        bg="#f8f9fa",
        relief="flat",
        highlightthickness=1,
        highlightbackground="#e0e0e0",
        highlightcolor="#5c7cfa"
    )
    chat_entry.pack(fill="x", padx=5, pady=5)

    def ai_reply(event=None):

        question = chat_entry.get().lower()

        X_test = vectorizer.transform([question])
        prediction = model.predict(X_test)[0]

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()


        # ---------- COUNT ----------
        if prediction == "count":

            cur.execute(
            "SELECT COUNT(*) FROM pending_payment_for_purchase"
            )

            c = cur.fetchone()[0]
            response = f"Total Pending = {c}"


        # ---------- LIST ----------
        elif prediction == "list":

            cur.execute(
            "SELECT customer_name FROM pending_payment_for_purchase"
            )

            rows = cur.fetchall()

            response = "Pending:\n" + "\n".join(
                [r[0] for r in rows]
            )


        # ---------- AMOUNT ----------
        elif prediction == "amount":

            cur.execute(
            "SELECT SUM(qty_of_product*price) FROM pending_payment_for_purchase"
            )

            total = cur.fetchone()[0]
            response = f"Total Amount = {total}"


        # ---------- QTY ----------
        elif prediction == "qty":

            cur.execute(
            "SELECT SUM(qty_of_product) FROM pending_payment_for_purchase"
            )

            total = cur.fetchone()[0]
            response = f"Total Qty = {total}"


        # ---------- TOP CUSTOMER ----------
        elif prediction == "customer":

            cur.execute("""
            SELECT customer_name,
            SUM(qty_of_product*price)
            FROM pending_payment_for_purchase
            GROUP BY customer_name
            ORDER BY 2 DESC LIMIT 1
            """)

            row = cur.fetchone()

            if row:
                response = f"Top Customer = {row[0]}"
            else:
                response = "No data"


        # ---------- TOP PRODUCT ----------
        elif prediction == "product":

            cur.execute("""
            SELECT product_name,
            SUM(qty_of_product)
            FROM pending_payment_for_purchase
            GROUP BY product_name
            ORDER BY 2 DESC LIMIT 1
            """)

            row = cur.fetchone()

            if row:
                response = f"Top Product = {row[0]}"
            else:
                response = "No data"


        # ---------- HIGHEST BILL ----------
        elif prediction == "highbill":

            cur.execute("""
            SELECT bill_no,
            SUM(qty_of_product*price)
            FROM pending_payment_for_purchase
            GROUP BY bill_no
            ORDER BY 2 DESC LIMIT 1
            """)

            row = cur.fetchone()
            response = f"Highest Bill = {row}"


        # ---------- LOWEST BILL ----------
        elif prediction == "lowbill":

            cur.execute("""
            SELECT bill_no,
            SUM(qty_of_product*price)
            FROM pending_payment_for_purchase
            GROUP BY bill_no
            ORDER BY 2 ASC LIMIT 1
            """)

            row = cur.fetchone()
            response = f"Lowest Bill = {row}"


        # ---------- AVERAGE ----------
        elif prediction == "average":

            cur.execute("""
            SELECT AVG(qty_of_product*price)
            FROM pending_payment_for_purchase
            """)

            avg = cur.fetchone()[0]
            response = f"Average Amount = {avg}"


        # ---------- TODAY ----------
        elif prediction == "today":

            today = datetime.now().strftime("%Y-%m-%d")

            cur.execute("""
            SELECT COUNT(*)
            FROM pending_payment_for_purchase
            WHERE date=?
            """, (today,))

            c = cur.fetchone()[0]
            response = f"Today Pending = {c}"


        # ---------- PAYMENT ----------
        elif prediction == "payment":

            cur.execute("""
            SELECT COUNT(*)
            FROM pending_payment_for_purchase
            WHERE payment_method='Pending'
            """)

            c = cur.fetchone()[0]
            response = f"Payment Pending = {c}"


        # ---------- OLD ----------
        elif prediction == "old":

            cur.execute(
            "SELECT date FROM pending_payment_for_purchase"
            )

            rows = cur.fetchall()

            response = f"Total records = {len(rows)}"


        # ---------- CUSTOMER LIST ----------
        elif prediction == "customerlist":

            cur.execute("""
            SELECT DISTINCT customer_name
            FROM pending_payment_for_purchase
            """)

            rows = cur.fetchall()

            response = "\n".join([r[0] for r in rows])


        # ---------- PRODUCT LIST ----------
        elif prediction == "productlist":

            cur.execute("""
            SELECT DISTINCT product_name
            FROM pending_payment_for_purchase
            """)

            rows = cur.fetchall()

            response = "\n".join([r[0] for r in rows])


        else:
            response = "I don't understand"


        conn.close()

        chat_display.insert(tk.END, "You : " + question)
        chat_display.insert(tk.END, "AI : " + str(response))

        chat_entry.delete(0, tk.END)
    
    chat_entry.bind("<Return>", ai_reply)
    black_btn(chat_frame, "ASK", "#5c7cfa", ai_reply).pack(pady=5)

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
           customer_name,
           date,
           payment_method,
           qty_of_product,
           price
    FROM pending_payment_for_purchase
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

        fields = [
    entry_purchase_bill,
    entry_bill_no,
    entry_product_id,
    entry_product_name,
    entry_customer_name,
    entry_date,
    entry_payment,
    entry_qty,
    entry_price
]

        for i, field in enumerate(fields):
            field.delete(0, tk.END)
            field.insert(0, row[i + 1])

    def save_entry():

        data = (
            entry_purchase_bill.get(),
            entry_bill_no.get(),
            entry_product_id.get(),
            entry_product_name.get(),
            entry_customer_name.get(),
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
            INSERT INTO pending_payment_for_purchase
            (purchase_bill, bill_no, product_id, product_name,
            customer_name, date, payment_method,
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
    UPDATE pending_payment_for_purchase
    SET purchase_bill=?, bill_no=?, product_id=?,
        product_name=?, customer_name=?, date=?,
        payment_method=?, qty_of_product=?, price=?
    WHERE rowid=?
""", (
    entry_purchase_bill.get(),
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
            cur.execute(
                "DELETE FROM pending_payment_for_purchase WHERE rowid=?",
                (selected_rowid,)
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Deleted", "Entry Deleted")
            clear_fields()
            show_data()

    def clear_fields():
        nonlocal selected_rowid
        selected_rowid = None

        for field in [
    entry_purchase_bill,
    entry_bill_no,
    entry_product_id,
    entry_product_name,
    entry_customer_name,
    entry_date,
    entry_payment,
    entry_qty,
    entry_price
]:
            field.delete(0, tk.END)

        entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

    def show_pending_buyer_analysis():

        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT * FROM pending_payment_for_purchase", conn)
        conn.close()

        if df.empty:
            messagebox.showinfo("Info", "No pending buyer payment data available")
            return

        # ---------------- Basic Calculations ----------------
        total_bills = df["bill_no"].nunique()
        total_quantity = df["qty_of_product"].sum()

        df["total_amount"] = df["qty_of_product"] * df["price"]
        total_pending_amount = df["total_amount"].sum()

        average_bill = total_pending_amount / total_bills if total_bills > 0 else 0

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

        # Highest pending date
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
        PENDING BUYER PAYMENT ANALYSIS
    ====================================

    🧾 Total Pending Bills         : {total_bills}
    📦 Total Pending Quantity      : {total_quantity}
    💰 Total Pending Amount        : ₹ {total_pending_amount:.2f}
    📊 Average Bill Amount         : ₹ {average_bill:.2f}

    ------------------------------------
    🏆 Most Purchased Pending Product
    ------------------------------------
    Product                        : {top_product}
    Quantity                       : {top_product_qty}

    ------------------------------------
    📉 Least Purchased Pending Product
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

        messagebox.showinfo("Pending Buyer Analysis", report)
    tree.bind("<<TreeviewSelect>>", select_record)
    show_data()
