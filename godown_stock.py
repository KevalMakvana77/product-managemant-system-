import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import fullscreen

def open_godown_stock_window():

    win = tk.Toplevel()
    win.title("Godown Stock")
    win.geometry("950x600")
    win.configure(bg="#f4f7fe")
    fullscreen.make_fullscreen(win)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "product_stock_name.db")

    selected_id = None

    # ================= HEADER =================
    header = tk.Frame(win, bg="#5c7cfa", height=80)
    header.pack(fill="x")

    tk.Label(header, text="GODOWN STOCK MANAGEMENT",
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

    entry_godown = create_input(form_frame, "Godown Name")
    entry_product_id = create_input(form_frame, "Product ID")

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

    black_btn("SAVE", lambda: save_stock()).pack(side="left", padx=5)
    black_btn("UPDATE", lambda: update_stock()).pack(side="left", padx=5)
    black_btn("DELETE", lambda: delete_stock()).pack(side="left", padx=5)

    # ================= TABLE =================
    columns = ("ID", "Godown Name", "Product ID")
    tree = ttk.Treeview(right_frame, columns=columns,
                        show="headings", height=15)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    tree.pack(fill="both", expand=True)

    # ================= LOGIC =================

    def show_data():
        for i in tree.get_children():
            tree.delete(i)

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM godown_stock")
        rows = cur.fetchall()
        conn.close()

        for row in rows:
            tree.insert("", tk.END, values=row)

    def select_record(event):
        nonlocal selected_id
        selected = tree.selection()
        if not selected:
            return

        row = tree.item(selected)['values']
        selected_id = row[0]

        entry_godown.delete(0, tk.END)
        entry_product_id.delete(0, tk.END)

        entry_godown.insert(0, row[1])
        entry_product_id.insert(0, row[2])

    def save_stock():
        if entry_godown.get() == "" or entry_product_id.get() == "":
            messagebox.showerror("Error", "All fields required")
            return

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO godown_stock (godown_name, product_id) VALUES (?,?)",
            (entry_godown.get(), entry_product_id.get())
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Saved", "Stock Added")
        clear_fields()
        show_data()

    def update_stock():
        if not selected_id:
            messagebox.showerror("Error", "Select record first")
            return

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("""
            UPDATE godown_stock
            SET godown_name=?, product_id=?
            WHERE id=?
        """, (entry_godown.get(), entry_product_id.get(), selected_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Updated", "Stock Updated")
        clear_fields()
        show_data()

    def delete_stock():
        if not selected_id:
            messagebox.showerror("Error", "Select record first")
            return

        if messagebox.askyesno("Confirm", "Delete this record?"):
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("DELETE FROM godown_stock WHERE id=?", (selected_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Deleted", "Record Deleted")
            clear_fields()
            show_data()

    def clear_fields():
        nonlocal selected_id
        selected_id = None
        entry_godown.delete(0, tk.END)
        entry_product_id.delete(0, tk.END)

    tree.bind("<<TreeviewSelect>>", select_record)
    show_data()
