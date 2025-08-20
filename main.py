import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import datetime

from db import init_db, insert_transaction, fetch_transactions
from auth import register_user, login_user
from visualization import plot_summary
from export import export_to_csv, export_to_excel

init_db()
current_user_id = None

def login_screen():
    def attempt_login():
        global current_user_id
        username = username_var.get()
        password = password_var.get()
        user_id = login_user(username, password)
        if user_id:
            current_user_id = user_id
            messagebox.showinfo("Login", f"Welcome {username}")
            login.destroy()
            main_app()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def attempt_register():
        username = username_var.get()
        password = password_var.get()
        if register_user(username, password):
            messagebox.showinfo("Success", "User registered! Please login.")
        else:
            messagebox.showerror("Error", "Username already exists.")

    login = tk.Tk()
    login.title("Login - Finance Tracker")
    login.geometry("300x200")

    tk.Label(login, text="Username").pack()
    username_var = tk.StringVar()
    tk.Entry(login, textvariable=username_var).pack()

    tk.Label(login, text="Password").pack()
    password_var = tk.StringVar()
    tk.Entry(login, textvariable=password_var, show="*").pack()

    tk.Button(login, text="Login", command=attempt_login).pack(pady=5)
    tk.Button(login, text="Register", command=attempt_register).pack()

    login.mainloop()

def main_app():
    root = tk.Tk()
    root.title("Personal Finance Tracker")
    root.geometry("700x500")

    # Transaction Form
    tk.Label(root, text="Type").grid(row=0, column=0)
    type_var = tk.StringVar(value="Expense")
    ttk.Combobox(root, textvariable=type_var, values=["Expense","Income"]).grid(row=0, column=1)

    tk.Label(root, text="Category").grid(row=1, column=0)
    category_var = tk.StringVar()
    tk.Entry(root, textvariable=category_var).grid(row=1, column=1)

    tk.Label(root, text="Amount").grid(row=2, column=0)
    amount_var = tk.DoubleVar()
    tk.Entry(root, textvariable=amount_var).grid(row=2, column=1)

    tk.Label(root, text="Date").grid(row=3, column=0)
    date_entry = DateEntry(root, width=12, background='darkblue', foreground='white')
    date_entry.grid(row=3, column=1)

    def add_transaction():
        insert_transaction(current_user_id, type_var.get(), category_var.get(), float(amount_var.get()), date_entry.get_date().strftime("%Y-%m-%d"))
        messagebox.showinfo("Success", "Transaction added")

    tk.Button(root, text="Add Transaction", command=add_transaction).grid(row=4, column=1)

    # Data Display
    tree = ttk.Treeview(root, columns=("ID","Type","Category","Amount","Date"), show="headings")
    for col in ("ID","Type","Category","Amount","Date"):
        tree.heading(col, text=col)
    tree.grid(row=6, column=0, columnspan=4)

    def refresh_data():
        for row in tree.get_children():
            tree.delete(row)
        transactions = fetch_transactions(current_user_id)
        for t in transactions:
            tree.insert("", tk.END, values=(t[0],t[2],t[3],t[4],t[5]))

    tk.Button(root, text="Refresh Data", command=refresh_data).grid(row=5, column=1)

    # Visualization
    tk.Button(root, text="Show Charts", command=lambda: plot_summary(current_user_id)).grid(row=7, column=1)

    # Export
    tk.Button(root, text="Export CSV", command=lambda: export_to_csv(current_user_id)).grid(row=8, column=0)
    tk.Button(root, text="Export Excel", command=lambda: export_to_excel(current_user_id)).grid(row=8, column=1)

    refresh_data()
    root.mainloop()

if __name__ == "__main__":
    login_screen()
