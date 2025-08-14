# ---------- Imports ----------
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import customtkinter as ctk
from tkinter import ttk, messagebox


# ---------- Google Sheets Setup ----------
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Load Google API credentials (DO NOT upload `sheet_credentials.json` to GitHub)
CREDS = ServiceAccountCredentials.from_json_keyfile_name("sheet_credentials.json", SCOPE)
CLIENT = gspread.authorize(CREDS)

# Open the Google Sheet by name (make sure it exists)
SHEET = CLIENT.open("TodoTasks").sheet1


# ---------- CRUD Operations ----------
def load_tasks():
    """Fetch all tasks from Google Sheets and return them as a list of dicts."""
    data = SHEET.get_all_records()
    return [{"title": row["Task"], "done": row["Done"] == "True"} for row in data]


def save_tasks():
    """Save the current tasks list to Google Sheets."""
    SHEET.clear()
    SHEET.append_row(["Task", "Done"])
    for task in tasks:
        SHEET.append_row([task["title"], str(task["done"])])


def refresh_table():
    """Refresh the UI table to display the latest tasks list."""
    for row in task_table.get_children():
        task_table.delete(row)

    for i, task in enumerate(tasks):
        status_icon = "✅" if task["done"] else "📦"
        task_table.insert("", "end", iid=i, values=(task["title"], status_icon))


def add_task():
    """Add a new task from the entry field to the tasks list."""
    title = entry_task.get().strip()
    if title:
        tasks.append({"title": title, "done": False})
        save_tasks()
        refresh_table()
        entry_task.delete(0, "end")
    else:
        messagebox.showwarning("Warning", "Task cannot be empty.")


def mark_done():
    """Mark the selected task as done."""
    selected = task_table.selection()
    if selected:
        idx = int(selected[0])
        tasks[idx]["done"] = True
        save_tasks()
        refresh_table()
    else:
        messagebox.showwarning("Warning", "Please select a task.")


def delete_task():
    """Delete the selected task from the list."""
    selected = task_table.selection()
    if selected:
        idx = int(selected[0])
        tasks.pop(idx)
        save_tasks()
        refresh_table()
    else:
        messagebox.showwarning("Warning", "Please select a task.")


# ---------- Theme Toggle ----------
def toggle_theme():
    """Switch between dark and light mode dynamically."""
    global MODE
    MODE = "light" if MODE == "dark" else "dark"
    ctk.set_appearance_mode(MODE)
    apply_table_style()
    refresh_table()
    btn_theme.configure(text="Light" if MODE == "dark" else "Dark")

def apply_table_style():
    """Apply table styles based on the current mode."""
    style = ttk.Style()
    style.theme_use("default")
    if MODE == "dark":
        style.configure(
            "Treeview",
            background="#2b2b2b",
            foreground="white",
            fieldbackground="#2b2b2b",
            rowheight=28,
            font=("Segoe UI", 11)
        )
        style.configure(
            "Treeview.Heading",
            background="#1f1f1f",
            foreground="white",
            font=("Segoe UI", 12, "bold")
        )
    else:
        style.configure(
            "Treeview",
            background="#EBEBEB",
            foreground="black",
            fieldbackground="#EBEBEB",
            rowheight=28,
            font=("Segoe UI", 11)
        )
        style.configure(
            "Treeview.Heading",
            background="#E3E3E3",
            foreground="black",
            font=("Segoe UI", 12, "bold")
        )
    style.map("Treeview", background=[("selected", "#1f538d")])


# ---------- UI Setup ----------
MODE = "dark"  # Default mode
ctk.set_appearance_mode(MODE)
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("To-Do List App (Google Sheets)")
root.geometry("500x400")

# ---------- Top Frame ----------
frame_top = ctk.CTkFrame(root)
frame_top.pack(fill="x", padx=10, pady=10)

entry_task = ctk.CTkEntry(frame_top, placeholder_text="Enter a new task...")
entry_task.pack(side="left", fill="x", expand=True, padx=(0, 5))

btn_add = ctk.CTkButton(frame_top, text="Add Task", command=add_task)
btn_add.pack(side="left")

btn_theme = ctk.CTkButton(frame_top, text="Light", width=40, command=toggle_theme)
btn_theme.pack(side="left", padx=(5, 0))

# ---------- Table ----------
frame_table = ctk.CTkFrame(root)
frame_table.pack(fill="both", expand=True, padx=10, pady=(0, 10))

apply_table_style()  # Apply initial theme styles

columns = ("Task", "Status")
task_table = ttk.Treeview(frame_table, columns=columns, show="headings", selectmode="browse")
task_table.heading("Task", text="Task")
task_table.heading("Status", text="Status")
task_table.column("Task", width=320, anchor="w")
task_table.column("Status", width=100, anchor="center")
task_table.pack(fill="both", expand=True)

# ---------- Bottom Frame ----------
frame_bottom = ctk.CTkFrame(root)
frame_bottom.pack(fill="x", padx=10, pady=(0, 10))

btn_done = ctk.CTkButton(frame_bottom, text="Mark Done", command=mark_done)
btn_done.pack(side="left", padx=5)

btn_delete = ctk.CTkButton(frame_bottom, text="Delete", fg_color="#d9534f", hover_color="#c9302c", command=delete_task)
btn_delete.pack(side="left", padx=5)

# ---------- Load Data & Start ----------
tasks = load_tasks()
refresh_table()

root.mainloop()
