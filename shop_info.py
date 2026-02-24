import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import fullscreen

def open_shop_info_window():

    win = tk.Toplevel()
    win.title("Shop Information")
    win.configure(bg="#f4f7fe")
    fullscreen.make_fullscreen(win)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "product_stock_name.db")

    selected_shop_id = 0   # ✅ FIXED

    # ================= HEADER =================
    header = tk.Frame(win, bg="#5c7cfa", height=80)
    header.pack(fill="x")

    tk.Label(header, text="SHOP INFORMATION MANAGEMENT",
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

    entry_name = create_input(form_frame, "Shop Name")
    entry_address = create_input(form_frame, "Address")
    entry_mobile = create_input(form_frame, "Mobile")

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

    black_btn("SAVE", lambda: save_info()).pack(side="left", padx=5)
    black_btn("UPDATE", lambda: update_info()).pack(side="left", padx=5)
    black_btn("DELETE", lambda: delete_info()).pack(side="left", padx=5)

    # ================= TABLE =================
    columns = ("ID", "Shop Name", "Address", "Mobile")

    tree = ttk.Treeview(right_frame, columns=columns,
                        show="headings", height=15)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=180)

    tree.pack(fill="both", expand=True)

    # ================= LOGIC =================

    def fetch_data():
        for i in tree.get_children():
            tree.delete(i)

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        cur.execute("SELECT * FROM shop_info")
        rows = cur.fetchall()

        print("Fetched Data:", rows)   # Debug line

        conn.close()

        for row in rows:
            tree.insert("", tk.END, values=row)

    def select_data(event):
        nonlocal selected_shop_id

        selected = tree.focus()   # ✅ FIXED
        if not selected:
            return

        row = tree.item(selected, "values")
        selected_shop_id = row[0]

        entry_name.delete(0, tk.END)
        entry_address.delete(0, tk.END)
        entry_mobile.delete(0, tk.END)

        entry_name.insert(0, row[1])
        entry_address.insert(0, row[2])
        entry_mobile.insert(0, row[3])

    def save_info():
        if entry_name.get() == "" or entry_address.get() == "" or entry_mobile.get() == "":
            messagebox.showerror("Error", "All fields required")
            return

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO shop_info (shop_name, address, mobile)
            VALUES (?,?,?)
        """, (entry_name.get(), entry_address.get(), entry_mobile.get()))
        conn.commit()
        conn.close()

        messagebox.showinfo("Saved", "Shop Info Added")
        clear_fields()
        fetch_data()

    def update_info():
        nonlocal selected_shop_id

        if selected_shop_id == 0:
            messagebox.showerror("Error", "Select record first")
            return

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("""
            UPDATE shop_info
            SET shop_name=?, address=?, mobile=?
            WHERE shop_id=?
        """, (entry_name.get(), entry_address.get(),
              entry_mobile.get(), selected_shop_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Updated", "Shop Info Updated")
        clear_fields()
        fetch_data()

    def delete_info():
        nonlocal selected_shop_id

        if selected_shop_id == 0:
            messagebox.showerror("Error", "Select record first")
            return

        if messagebox.askyesno("Confirm", "Delete this shop info?"):
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("DELETE FROM shop_info WHERE shop_id=?", (selected_shop_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Deleted", "Shop Info Deleted")
            clear_fields()
            fetch_data()

    def clear_fields():
        nonlocal selected_shop_id
        selected_shop_id = 0
        entry_name.delete(0, tk.END)
        entry_address.delete(0, tk.END)
        entry_mobile.delete(0, tk.END)

    tree.bind("<<TreeviewSelect>>", select_data)
    fetch_data()
