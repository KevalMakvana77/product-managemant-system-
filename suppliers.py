import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import pandas as pd
import fullscreen

def open_open_Suppliers_window():

    win = tk.Toplevel()
    win.title("Supplier Management")
    win.geometry("950x600")
    win.configure(bg="#f4f7fe")
    fullscreen.make_fullscreen(win)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "product_stock_name.db")

    selected_supplier_id = None

    # ================= HEADER =================
    header = tk.Frame(win, bg="#5c7cfa", height=80)
    header.pack(fill="x", side="top")

    tk.Label(header, text="SUPPLIER MANAGEMENT",
             font=("Helvetica", 18, "bold"),
             bg="#5c7cfa", fg="white").pack(pady=20)

    # ================= MAIN CARD =================
    main_frame = tk.Frame(win, bg="white", padx=25, pady=20,
                          highlightbackground="#e0e0e0",
                          highlightthickness=1)
    main_frame.place(relx=0.5, rely=0.55, anchor="center",
                     width=1200, height=800)

    # ================= LEFT FORM =================
    form_frame = tk.Frame(main_frame, bg="white")
    form_frame.pack(side="left", fill="y", padx=20)

    def create_input(parent, label_text):
        tk.Label(parent, text=label_text,
                 font=("Segoe UI", 10, "bold"),
                 bg="white", fg="#5c7cfa").pack(anchor="w", pady=(5, 5))

        entry = tk.Entry(parent, font=("Segoe UI", 10),
                         bg="#f8f9fa", relief="flat",
                         highlightthickness=1,
                         highlightbackground="#e0e0e0",
                         highlightcolor="#5c7cfa")
        entry.pack(fill="x", ipady=6, pady=(0, 10))
        return entry

    entry_name = create_input(form_frame, "Supplier Name")
    entry_mobile = create_input(form_frame, "Mobile Number")
    entry_email = create_input(form_frame, "Email")
    entry_gst = create_input(form_frame, "GST")
    entry_group = create_input(form_frame, "Group")
    entry_address = create_input(form_frame, "Address")
    entry_city = create_input(form_frame, "City")
    entry_pincode = create_input(form_frame, "Pincode")


    # ================= RIGHT SIDE =================
    right_frame = tk.Frame(main_frame, bg="white")
    right_frame.pack(side="right", fill="both", expand=True, padx=20)

    # Buttons
    btn_frame = tk.Frame(right_frame, bg="white")
    btn_frame.pack(fill="x", pady=(0, 15))

    def btn_style(parent, text, color, cmd):
        return tk.Button(parent, text=text, command=cmd,
                         bg=color, fg="black",
                         font=("Segoe UI", 9, "bold"),
                         relief="flat", cursor="hand2",
                         width=12, pady=6)

    btn_style(btn_frame, "SAVE", "#5c7cfa", lambda: add_supplier()).pack(side="left", padx=5)
    btn_style(btn_frame, "UPDATE", "#4c6ef5", lambda: update_supplier()).pack(side="left", padx=5)
    btn_style(btn_frame, "DELETE", "#fa5252", lambda: delete_supplier()).pack(side="left", padx=5)
    btn_style(btn_frame, "ANALYSIS", "#fa5252", lambda: show_supplier_analysis()).pack(side="left", padx=5)

    # Treeview Table
    columns = ("ID","Name","Mobile","Group","Address","City","Pincode","Email","GST")

    tree = ttk.Treeview(right_frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    tree.pack(fill="both", expand=True)


    # ================= LOGIC =================

    def show_suppliers():
        for i in tree.get_children():
            tree.delete(i)

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM suppliers")
        rows = cur.fetchall()
        conn.close()

        for row in rows:
            tree.insert("", tk.END, values=row)

    def select_supplier(event):
        nonlocal selected_supplier_id

        selected = tree.selection()
        if not selected:
            return

        values = tree.item(selected)['values']
        selected_supplier_id = values[0]

        # Clear fields first
        entry_name.delete(0, tk.END)
        entry_mobile.delete(0, tk.END)
        entry_group.delete(0, tk.END)
        entry_address.delete(0, tk.END)
        entry_city.delete(0, tk.END)
        entry_pincode.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_gst.delete(0, tk.END)

        # Insert all values
        entry_name.insert(0, values[1])
        entry_mobile.insert(0, values[2])
        entry_group.insert(0, values[3])
        entry_address.insert(0, values[4])
        entry_city.insert(0, values[5])
        entry_pincode.insert(0, values[6])
        entry_email.insert(0, values[7])
        entry_gst.insert(0, values[8])

    def add_supplier():
        name = entry_name.get().strip()
        mobile = entry_mobile.get().strip()
        group = entry_group.get().strip()
        address = entry_address.get().strip()
        city = entry_city.get().strip()
        pincode = entry_pincode.get().strip()
        email = entry_email.get().strip()
        gst = entry_gst.get().strip() or None

        if name == "" or mobile == "":
            messagebox.showerror("Error", "Name and Mobile required")
            return

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO suppliers
            (supplier_name, mobile, supplier_group, address, city, pincode, email, gstno)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, mobile, group, address, city, pincode, email, gst))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Supplier Added Successfully")
        clear_fields()
        show_suppliers()

    def update_supplier():
        if not selected_supplier_id:
            messagebox.showerror("Error", "Select supplier first")
            return

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        cur.execute("""
            UPDATE suppliers
            SET supplier_name=?, mobile=?, supplier_group=?, address=?, city=?, pincode=?, email=?, gstno=?
            WHERE supplier_id=?
        """, (
            entry_name.get(),
            entry_mobile.get(),
            entry_group.get(),
            entry_address.get(),
            entry_city.get(),
            entry_pincode.get(),
            entry_email.get(),
            entry_gst.get(),
            selected_supplier_id
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Supplier Updated Successfully")
        clear_fields()
        show_suppliers()

    def delete_supplier():
        if not selected_supplier_id:
            messagebox.showerror("Error", "Select supplier first")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete?"):
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("DELETE FROM suppliers WHERE supplier_id=?", (selected_supplier_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Supplier Deleted")
            clear_fields()
            show_suppliers()

    def clear_fields():
        nonlocal selected_supplier_id
        selected_supplier_id = None

        entry_name.delete(0, tk.END)
        entry_mobile.delete(0, tk.END)
        entry_group.delete(0, tk.END)
        entry_address.delete(0, tk.END)
        entry_city.delete(0, tk.END)
        entry_pincode.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_gst.delete(0, tk.END)

        tree.selection_remove(tree.selection())

    def show_supplier_analysis():
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT * FROM suppliers", conn)
        conn.close()

        if df.empty:
            messagebox.showinfo("Info", "No supplier data available")
            return

        total_suppliers = len(df)

         # Badha duplicate rows select karva
        duplicate_rows = df[df["mobile"].duplicated(keep=False)]

        # Unique duplicate mobile numbers medava
        duplicate_mobiles = duplicate_rows["mobile"].unique().tolist()

        # Clean text banavvu
        duplicate_text = ", ".join(duplicate_mobiles) if duplicate_mobiles else "None"

        # ---------------- Name Insights ----------------
        df["supplier_name"] = df["supplier_name"].fillna("")

        longest_name = df.loc[
            df["supplier_name"].str.len().idxmax(), "supplier_name"
        ]

        shortest_name = df.loc[
            df["supplier_name"].str.len().idxmin(), "supplier_name"
        ]

        # ---------------- GST Analysis ----------------
       # ---------------- GST Analysis ----------------
        if "gstno" in df.columns:

            # First handle real NULL values properly
            df["gstno"] = df["gstno"].fillna("")

            # Convert to string and remove spaces
            df["gstno"] = df["gstno"].astype(str).str.strip()

            # Make everything lowercase for safe comparison
            df["gstno"] = df["gstno"].str.lower()

            # Invalid GST values
            invalid_values = ["", "none", "null", "nan"]

            gst_count = (~df["gstno"].isin(invalid_values)).sum()
            gst_not_filled = total_suppliers - gst_count

        else:
            gst_count = 0
            gst_not_filled = total_suppliers

        # ---------------- City Wise Analysis ----------------
        if "city" in df.columns and df["city"].notna().any():
            city_counts = df["city"].value_counts()
            top_city = city_counts.idxmax()
            top_city_count = city_counts.max()
        else:
            top_city = "N/A"
            top_city_count = 0

        report = f"""
    ====================================
            SUPPLIER ANALYSIS
    ====================================

    🏢 Total Suppliers            : {total_suppliers}

    ------------------------------------
    📱 Contact Insights
    ------------------------------------
    Duplicate Mobile Numbers      : {duplicate_text}

    ------------------------------------
    📝 Name Insights
    ------------------------------------
    Longest Supplier Name         : {longest_name}
    Shortest Supplier Name        : {shortest_name}

    ------------------------------------
    🧾 GST Insights
    ------------------------------------
    Suppliers With GST            : {gst_count}
    Suppliers Without GST         : {gst_not_filled}

    ------------------------------------
    🏙 City Insights
    ------------------------------------
    Top Supplier City             : {top_city}
    Suppliers From Top City       : {top_city_count}

    ====================================
    """

        messagebox.showinfo("Supplier Analysis", report)



    tree.bind("<<TreeviewSelect>>", select_supplier)
    show_suppliers()
