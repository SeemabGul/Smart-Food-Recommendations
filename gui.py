import tkinter as tk
from login import open_login


def main():
    window = tk.Tk()
    window.title("Smart Food Recommendation System")
    window.geometry("1000x650")
    window.configure(bg="#F4F6F9")

    header = tk.Label(
        window,
        text="Smart Food Recommendation System",
        font=("Arial", 24, "bold"),
        bg="#2E7D32",
        fg="white",
        pady=15
    )
    header.pack(fill="x")

    subtitle = tk.Label(
        window,
        text="Eat smart. Live better.",
        font=("Arial", 14),
        bg="#F4F6F9",
        fg="#333333"
    )
    subtitle.pack(pady=20)

    start_btn = tk.Button(
        window,
        text="Get Started",
        font=("Arial", 14, "bold"),
        bg="#43A047",
        fg="white",
        width=20,
        command=lambda: open_login(window)
    )
    start_btn.pack(pady=30)

    window.mainloop()


if __name__ == "__main__":
    main()
