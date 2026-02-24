import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import fullscreen
import pandas as pd

def open_categories_window():

    win = tk.Toplevel()
    win.title("Category Management")
    win.geometry("900x550")
    win.configure(bg="#f4f7fe")
    fullscreen.make_fullscreen(win)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "product_stock_name.db")

    selected_category_id = None

    # ================= HEADER =================
    header = tk.Frame(win, bg="#5c7cfa", height=80)
    header.pack(fill="x")

    tk.Label(header, text="CATEGORY MANAGEMENT",
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

    tk.Label(form_frame, text="Category Name",
             font=("Segoe UI", 10, "bold"),
             bg="white", fg="#5c7cfa").pack(anchor="w", pady=(5, 5))

    entry_category = tk.Entry(form_frame,
                              font=("Segoe UI", 10),
                              bg="#f8f9fa",
                              relief="flat",
                              highlightthickness=1,
                              highlightbackground="#e0e0e0",
                              highlightcolor="#5c7cfa")
    entry_category.pack(fill="x", ipady=6)

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

    black_btn("SAVE", lambda: add_category()).pack(side="left", padx=5)
    black_btn("UPDATE", lambda: update_category()).pack(side="left", padx=5)
    black_btn("DELETE", lambda: delete_category()).pack(side="left", padx=5)
    black_btn("ANAYLSIS", lambda: show_category_summary()).pack(side="left", padx=5)

    # ================= TABLE =================
    columns = ("ID", "Category Name")
    tree = ttk.Treeview(right_frame, columns=columns,
                        show="headings", height=12)

    tree.heading("ID", text="ID")
    tree.heading("Category Name", text="Category Name")

    tree.column("ID", width=80)
    tree.column("Category Name", width=200)

    tree.pack(fill="both", expand=True)

    # ================= LOGIC =================

    def fetch_categories():
        for i in tree.get_children():
            tree.delete(i)

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM categories")
        rows = cur.fetchall()
        conn.close()

        for row in rows:
            tree.insert("", tk.END, values=row)

    def select_category(event):
        nonlocal selected_category_id
        selected = tree.selection()
        if not selected:
            return

        row = tree.item(selected)['values']
        selected_category_id = row[0]

        entry_category.delete(0, tk.END)
        entry_category.insert(0, row[1])

    def add_category():
        if entry_category.get() == "":
            messagebox.showerror("Error", "Category name required")
            return

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("INSERT INTO categories (category_name) VALUES (?)",
                    (entry_category.get(),))
        conn.commit()
        conn.close()

        entry_category.delete(0, tk.END)
        fetch_categories()

    def update_category():
        if not selected_category_id:
            messagebox.showerror("Error", "Select category first")
            return

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("UPDATE categories SET category_name=? WHERE category_id=?",
                    (entry_category.get(), selected_category_id))
        conn.commit()
        conn.close()

        entry_category.delete(0, tk.END)
        fetch_categories()

    def delete_category():
        if not selected_category_id:
            messagebox.showerror("Error", "Select category first")
            return

        if messagebox.askyesno("Confirm", "Delete this category?"):
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("DELETE FROM categories WHERE category_id=?",
                        (selected_category_id,))
            conn.commit()
            conn.close()

            entry_category.delete(0, tk.END)
            fetch_categories()

    def show_category_summary():

        conn = sqlite3.connect(db_path)

        df = pd.read_sql_query("SELECT category_name FROM categories", conn)
        conn.close()

        # Clean + Sort
        df["category_name"] = df["category_name"].str.strip()
        df = df.sort_values("category_name")

        total = len(df)

        # Badha duplicate rows select karva
        duplicate_rows = df[df.duplicated("category_name", keep=False)]

        # Unique duplicate category names medava
        duplicate_names = duplicate_rows["category_name"].unique().tolist()

        duplicate_text = ", ".join(duplicate_names) if duplicate_names else "None"

        # Unique categories only
        unique_categories = df["category_name"].drop_duplicates().tolist()

        # Proper formatted list
        category_text = ""
        for i, name in enumerate(unique_categories, 1):
            category_text += f"{i}. {name}\n"

        report = f"""
        ================================
                CATEGORY SUMMARY
        ================================

        📦 Total Categories     : {total}
        ⚠ Duplicate Categories : {duplicate_text}

        --------------------------------
        📂 Category Names:
        {category_text}
        """

        messagebox.showinfo("Category Summary", report)

    tree.bind("<<TreeviewSelect>>", select_category)
    fetch_categories()
