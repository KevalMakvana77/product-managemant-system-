import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
from datetime import datetime
import pandas as pd
import fullscreen
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import numpy as np

def open_Stock_in_window():

    win = tk.Toplevel()
    win.title("Stock In Management")
    win.geometry("1000x620")
    win.configure(bg="#f4f7fe")
    fullscreen.make_fullscreen(win)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "product_stock_name.db")

    selected_stock_id = None

    # ---------- AI TRAINING ----------

    training_questions = [

    "total stock",
    "how many stock",
    "stock count",
    "stock records",

    "list stock",
    "show stock",
    "all stock",
    "stock list",

    "stock of product",
    "product stock",
    "how much product",
    "product quantity",

    "supplier stock",
    "stock by supplier",
    "supplier quantity",
    "who supplied",

    "stock date",
    "date stock",
    "stock on date",

    "total quantity",
    "sum quantity",
    "all quantity",

    "find product",
    "search product",
    "stock of pen",
    "stock of mouse",

    "find supplier",
    "search supplier",

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

    "product",
    "product",
    "product",
    "product",

    "supplier",
    "supplier",
    "supplier",
    "supplier",

    "date",
    "date",
    "date",

    "qty",
    "qty",
    "qty",

    "product",
    "product",
    "product",
    "product",

    "supplier",
    "supplier",

    ]

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(training_questions)

    model = LogisticRegression()
    model.fit(X, training_labels)

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
    
    tk.Label(form_frame, text="Product Name",
            font=("Segoe UI", 10, "bold"),
            bg="white", fg="#5c7cfa").pack(anchor="w", pady=(5, 5))

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT product_name FROM products")

    products = [row[0] for row in cur.fetchall()]

    conn.close()

    entry_product_name = ttk.Combobox(
        form_frame,
        values=products,
        font=("Segoe UI", 10),
        state="readonly"
    )

    entry_product_name.pack(fill="x", ipady=6, pady=(0, 10))
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
    btn_style(btn_frame, "LOGOUT", "#fa5252", lambda: win.destroy()).pack(side="right", padx=5)

    # Treeview
    columns = ("ID", "Product Name", "Supplier Name", "Quantity", "Date")
    tree = ttk.Treeview(right_frame, columns=columns, show="headings", height=15)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

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


    entry_chat = tk.Entry(
        chat_frame,
        font=("Segoe UI", 10),
        bg="#f8f9fa",
        relief="flat",
        highlightthickness=1,
        highlightbackground="#e0e0e0",
        highlightcolor="#5c7cfa"
    )
    entry_chat.pack(fill="x", padx=5, pady=5)

    def chatbot_response(event=None):

        user_input = entry_chat.get().lower()
        entry_chat.delete(0, tk.END)

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        X_test = vectorizer.transform([user_input])
        prediction = model.predict(X_test)[0]

        response = "Not found"


        # ---------- COUNT ----------
        if prediction == "count":

            cur.execute("SELECT COUNT(*) FROM stock_in")
            c = cur.fetchone()[0]

            response = f"Total records = {c}"


        # ---------- LIST ----------
        elif prediction == "list":

            cur.execute("SELECT product_name, quantity FROM stock_in")
            rows = cur.fetchall()

            text = ""
            for r in rows:
                text += f"{r[0]} = {r[1]}\n"

            response = text


        # ---------- PRODUCT SEARCH ----------
        elif prediction == "product":

            words = user_input.split()

            for w in words:

                cur.execute("""
                SELECT product_name, quantity, supplier_name, date
                FROM stock_in
                WHERE product_name LIKE ?
                """, ('%' + w + '%',))

                row = cur.fetchone()

                if row:
                    response = f"""
    Product : {row[0]}
    Qty : {row[1]}
    Supplier : {row[2]}
    Date : {row[3]}
    """
                    break


        # ---------- SUPPLIER SEARCH ----------
        elif prediction == "supplier":

            words = user_input.split()

            for w in words:

                cur.execute("""
                SELECT product_name, quantity, supplier_name
                FROM stock_in
                WHERE supplier_name LIKE ?
                """, ('%' + w + '%',))

                row = cur.fetchone()

                if row:
                    response = f"""
    Supplier : {row[2]}
    Product : {row[0]}
    Qty : {row[1]}
    """
                    break


        # ---------- DATE SEARCH ----------
            # DATE SEARCH
        elif prediction == "date":

            words = user_input.split()

            found = False

            for w in words:

                cur.execute("""
                SELECT product_name, quantity, date
                FROM stock_in
                WHERE date LIKE ?
                """, ('%' + w + '%',))

                row = cur.fetchone()

                if row:
                    response = f"""
    Product : {row[0]}
    Qty : {row[1]}
    Date : {row[2]}
    """
                    found = True
                    break

            if not found:
                response = "No stock found for that date"


        # ---------- TOTAL QTY ----------
        elif prediction == "qty":

            cur.execute("SELECT SUM(quantity) FROM stock_in")
            total = cur.fetchone()[0]

            response = f"Total quantity = {total}"


        conn.close()

        chat_display.insert(tk.END, "You: " + user_input)
        chat_display.insert(tk.END, "Bot: " + str(response))
        chat_display.insert(tk.END, "--------------")
    
    entry_chat.bind("<Return>", chatbot_response)
    btn_style(chat_frame, "ASK", "#5c7cfa", chatbot_response).pack(pady=5)

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

        entry_product_name.delete(0, tk.END)
        entry_supplier_name.delete(0, tk.END)
        entry_qty.delete(0, tk.END)
        entry_date.delete(0, tk.END)

        entry_product_name.insert(0, values[1])
        entry_supplier_name.insert(0, values[2])
        entry_qty.insert(0, values[3])
        entry_date.insert(0, values[4])

    def add_stock():
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("""INSERT INTO stock_in (product_name, supplier_name, quantity, date)
        VALUES (?,?,?,?)""",
        (entry_product_name.get(), entry_supplier_name.get(),
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
        cur.execute("""UPDATE stock_in SET product_name=?, supplier_name=?, quantity=?, date=?
        WHERE stock_in_id=?""",
        (entry_product_name.get(), entry_supplier_name.get(),
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
        entry_product_name.delete(0, tk.END)
        entry_supplier_name.delete(0, tk.END)
        entry_qty.delete(0, tk.END)
        entry_date.delete(0, tk.END)
        entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

    def show_stock_report():

        conn = sqlite3.connect(db_path)

        # Database mathi stock_in data lao
        df = pd.read_sql_query("SELECT * FROM stock_in", conn)
        conn.close()

        if df.empty:
            messagebox.showinfo("Stock Report", "No stock data found!")
            return

        # 🔹 Total Stock Quantity
        total_stock = df["quantity"].sum()

        # 🔹 Product ID wise total stock
        product_summary = df.groupby("product_id")["quantity"].sum()

        # 🔹 Supplier wise total stock  ✅ NEW
        supplier_summary = df.groupby("supplier_name")["quantity"].sum()

        # 🔹 Date wise total stock
        date_summary = df.groupby("date")["quantity"].sum()

        # 🔹 Highest stock product
        highest_product = product_summary.idxmax()
        highest_quantity = product_summary.max()

        # 🔹 Top Supplier  ✅ NEW
        top_supplier = supplier_summary.idxmax()
        top_supplier_qty = supplier_summary.max()

        # ---------------- Product Summary Text ----------------
        product_text = ""
        for pid, qty in product_summary.items():
            product_text += f"Product ID {pid}  →  {qty}\n"

        # ---------------- Supplier Summary Text ----------------
        supplier_text = ""
        for name, qty in supplier_summary.items():
            supplier_text += f"{name}  →  {qty}\n"

        # ---------------- Date Summary Text ----------------
        date_text = ""
        for d, qty in date_summary.items():
            date_text += f"{d}  →  {qty}\n"

        # ---------------- Final Report ----------------
        report = f"""
        ====================================
                    STOCK REPORT
        ====================================

        📦 Total Stock Quantity : {total_stock}

        🏆 Highest Stock Product ID : {highest_product}
        Quantity : {highest_quantity}

        🥇 Top Supplier : {top_supplier}
        Quantity Supplied : {top_supplier_qty}

        ------------------------------------
        📊 Stock Per Product ID:
        {product_text}

        ------------------------------------
        🏢 Stock Per Supplier:
        {supplier_text}

        ------------------------------------
        📅 Stock Per Date:
        {date_text}
        """

        messagebox.showinfo("Stock Report", report)

    tree.bind("<<TreeviewSelect>>", select_stock)
    show_stock()
