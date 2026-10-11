import tkinter as tk
from tkinter import ttk, messagebox
from recommender import get_recommendations
from user_data import get_user, save_preferences, add_history_entry, get_history

try:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    CHARTS_AVAILABLE = True
except ImportError:
    CHARTS_AVAILABLE = False


def open_dashboard(parent, username="Guest"):
    dashboard = tk.Toplevel(parent)
    dashboard.title("Dashboard")
    dashboard.geometry("780x700")
    dashboard.configure(bg="#F4F6F9")

    user = get_user(username)
    prefs = user.get("preferences", {})
    current_results = []

    header = tk.Label(
        dashboard,
        text=f"Welcome, {username}!",
        font=("Arial", 20, "bold"),
        bg="#2E7D32",
        fg="white",
        pady=12
    )
    header.pack(fill="x")

    form_frame = tk.Frame(dashboard, bg="#F4F6F9")
    form_frame.pack(pady=15)

    tk.Label(form_frame, text="Diet Type:", bg="#F4F6F9", font=("Arial", 12)).grid(
        row=0, column=0, padx=10, pady=8, sticky="w"
    )
    diet_var = tk.StringVar(value=prefs.get("diet_type", "Any"))
    diet_menu = ttk.Combobox(
        form_frame, textvariable=diet_var,
        values=["Any", "Vegetarian", "Vegan", "Non-Vegetarian"],
        width=22, state="readonly"
    )
    diet_menu.grid(row=0, column=1, padx=10, pady=8)

    tk.Label(form_frame, text="Max Calories:", bg="#F4F6F9", font=("Arial", 12)).grid(
        row=1, column=0, padx=10, pady=8, sticky="w"
    )
    calorie_entry = tk.Entry(form_frame, width=24)
    calorie_entry.insert(0, str(prefs.get("max_calories", 500)))
    calorie_entry.grid(row=1, column=1, padx=10, pady=8)

    tk.Label(form_frame, text="Avoid Ingredients:", bg="#F4F6F9", font=("Arial", 12)).grid(
        row=2, column=0, padx=10, pady=8, sticky="w"
    )
    allergy_entry = tk.Entry(form_frame, width=24)
    allergy_entry.insert(0, ", ".join(prefs.get("allergies", [])))
    allergy_entry.grid(row=2, column=1, padx=10, pady=8)

    tk.Label(
        form_frame, text="(comma separated, e.g. dairy, nuts, egg)",
        bg="#F4F6F9", font=("Arial", 9), fg="#666666"
    ).grid(row=3, column=1, sticky="w", padx=10)

    result_box = tk.Listbox(dashboard, width=85, height=12, font=("Arial", 11))
    result_box.pack(pady=15)

    status_label = tk.Label(dashboard, text="", bg="#F4F6F9", font=("Arial", 10), fg="#333333")
    status_label.pack()

    def show_recommendations():
        nonlocal current_results
        result_box.delete(0, tk.END)
        diet = diet_var.get()
        try:
            max_cal = int(calorie_entry.get())
        except ValueError:
            result_box.insert(tk.END, "Please enter a valid number for calories.")
            return

        allergies = [a.strip() for a in allergy_entry.get().split(",") if a.strip()]
        results = get_recommendations(diet, max_cal, exclude_allergens=allergies)
        current_results = results

        if not results:
            result_box.insert(tk.END, "No matching foods found.")
        else:
            for item in results:
                result_box.insert(
                    tk.END,
                    f"{item['food_name']}  |  {item['category']}  |  {item['calories']} kcal"
                )

        save_preferences(username, diet, max_cal, allergies)
        add_history_entry(username, results)
        status_label.config(text=f"Found {len(results)} matching foods  \u2022  saved to your history")

    def show_history():
        history = get_history(username)
        hist_win = tk.Toplevel(dashboard)
        hist_win.title("Search History")
        hist_win.geometry("520x420")
        hist_win.configure(bg="#F4F6F9")

        tk.Label(
            hist_win, text="Your Recent Searches", font=("Arial", 14, "bold"),
            bg="#2E7D32", fg="white", pady=8
        ).pack(fill="x")

        if not history:
            tk.Label(
                hist_win, text="No search history yet.", bg="#F4F6F9", font=("Arial", 11)
            ).pack(pady=20)
            return

        listbox = tk.Listbox(hist_win, width=65, height=16, font=("Arial", 10))
        listbox.pack(pady=10)
        for entry in history:
            foods_preview = ", ".join(entry["foods"][:3]) if entry["foods"] else "no matches"
            listbox.insert(
                tk.END,
                f"{entry['timestamp']}  \u2014  {entry['count']} results  ({foods_preview})"
            )

    def show_chart():
        if not current_results:
            messagebox.showinfo("No Data", "Get recommendations first to see a chart.")
            return
        if not CHARTS_AVAILABLE:
            messagebox.showwarning(
                "Charts Unavailable",
                "Install matplotlib to enable charts:\n\npip install matplotlib"
            )
            return

        chart_win = tk.Toplevel(dashboard)
        chart_win.title("Calorie Chart")
        chart_win.geometry("720x520")
        chart_win.configure(bg="#F4F6F9")

        names = [r["food_name"] for r in current_results][:10]
        calories = [r["calories"] for r in current_results][:10]

        fig = Figure(figsize=(6.6, 4.4), dpi=100)
        ax = fig.add_subplot(111)
        ax.barh(names, calories, color="#43A047")
        ax.set_xlabel("Calories")
        ax.set_title("Calories by Food Item")
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=chart_win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    btn_frame = tk.Frame(dashboard, bg="#F4F6F9")
    btn_frame.pack(pady=10)

    tk.Button(
        btn_frame, text="Get Recommendations", command=show_recommendations,
        bg="#43A047", fg="white", font=("Arial", 12, "bold"), width=20
    ).grid(row=0, column=0, padx=6)

    tk.Button(
        btn_frame, text="View History", command=show_history,
        bg="#2E7D32", fg="white", font=("Arial", 12, "bold"), width=14
    ).grid(row=0, column=1, padx=6)

    tk.Button(
        btn_frame, text="Show Chart", command=show_chart,
        bg="#6D4C41", fg="white", font=("Arial", 12, "bold"), width=14
    ).grid(row=0, column=2, padx=6)
