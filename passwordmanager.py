import json
import os
import random
import string
import tkinter as tk
from tkinter import messagebox

PASSWORD_FILE = "passwords.json"

def load_passwords():
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r") as f:
            return json.load(f)
    return {}

def save_passwords(passwords):
    with open(PASSWORD_FILE, "w") as f:
        json.dump(passwords, f)

def add_password():
    account = entry_account.get().strip()
    username = entry_username.get().strip()
    password = entry_password.get().strip()

    if not account or not username or not password:
        messagebox.showwarning("Warning", "Please fill all fields!")
        return

    passwords = load_passwords()
    passwords[account] = {"username": username, "password": password}
    save_passwords(passwords)
    messagebox.showinfo("Success", f"Password for '{account}' saved!")

    entry_account.delete(0, tk.END)
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    refresh_list()

def view_password():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Warning", "Please select an account!")
        return

    account = listbox.get(selected[0])
    passwords = load_passwords()
    info = passwords[account]
    messagebox.showinfo("Details", f"Account : {account}\nUsername: {info['username']}\nPassword: {info['password']}")

def delete_password():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Warning", "Please select an account!")
        return

    account = listbox.get(selected[0])
    confirm = messagebox.askyesno("Confirm", f"Delete '{account}'?")
    if confirm:
        passwords = load_passwords()
        del passwords[account]
        save_passwords(passwords)
        messagebox.showinfo("Deleted", f"'{account}' deleted!")
        refresh_list()

def generate_password():
    chars = string.ascii_letters + string.digits + "!@#$%"
    pwd = "".join(random.choice(chars) for i in range(12))
    entry_password.delete(0, tk.END)
    entry_password.insert(0, pwd)

def refresh_list():
    listbox.delete(0, tk.END)
    passwords = load_passwords()
    for account in passwords:
        listbox.insert(tk.END, account)

window = tk.Tk()
window.title("Password Manager")
window.geometry("420x480")
window.config(bg="#f0f0f0")

tk.Label(window, text="Password Manager", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)

tk.Label(window, text="Account Name:", bg="#f0f0f0").pack()
entry_account = tk.Entry(window, width=35)
entry_account.pack(pady=3)

tk.Label(window, text="Username/Email:", bg="#f0f0f0").pack()
entry_username = tk.Entry(window, width=35)
entry_username.pack(pady=3)

tk.Label(window, text="Password:", bg="#f0f0f0").pack()
entry_password = tk.Entry(window, width=35, show="*")
entry_password.pack(pady=3)

tk.Button(window, text="Save Password", width=15, bg="#4CAF50", fg="white", command=add_password).pack(pady=5)
tk.Button(window, text="Generate Password", width=15, bg="#2196F3", fg="white", command=generate_password).pack(pady=2)

tk.Label(window, text="Saved Accounts:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(pady=5)

listbox = tk.Listbox(window, width=40, height=7)
listbox.pack(pady=3)

tk.Button(window, text="View Password", width=15, bg="#FF9800", fg="white", command=view_password).pack(pady=3)
tk.Button(window, text="Delete Password", width=15, bg="#f44336", fg="white", command=delete_password).pack(pady=2)

refresh_list()
window.mainloop()