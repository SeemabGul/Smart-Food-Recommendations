import tkinter as tk
from dashboard import open_dashboard


def open_login(parent):
    login = tk.Toplevel(parent)
    login.title("Login")
    login.geometry("500x400")
    login.configure(bg="#F4F6F9")

    title = tk.Label(
        login,
        text="User Login",
        font=("Arial", 20, "bold"),
        bg="#2E7D32",
        fg="white",
        pady=10
    )
    title.pack(fill="x")

    tk.Label(
        login,
        text="Username",
        bg="#F4F6F9",
        font=("Arial", 12)
    ).pack(pady=10)

    username = tk.Entry(login, width=30)
    username.pack()

    tk.Label(
        login,
        text="Password",
        bg="#F4F6F9",
        font=("Arial", 12)
    ).pack(pady=10)

    password = tk.Entry(login, show="*", width=30)
    password.pack()

    status_label = tk.Label(login, text="", bg="#F4F6F9", fg="red")
    status_label.pack()

    def handle_login():
        user = username.get().strip()
        if user == "":
            status_label.config(text="Please enter a username")
            return
        login.destroy()
        open_dashboard(parent, user)

    tk.Button(
        login,
        text="Login",
        command=handle_login,
        bg="#43A047",
        fg="white",
        width=20
    ).pack(pady=10)
