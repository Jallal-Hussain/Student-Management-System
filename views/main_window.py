# ===== MAIN WINDOW ===== #

import tkinter as tk
from datetime import datetime
from views.form import StudentForm
from views.table import StudentTableView
from constants import THEME


class StudentManagementSystem:
    def __init__(self, root, db_manager):
        self.root = root
        self.db_manager = db_manager
        self.theme = THEME
        self.setup_window()
        self.create_widgets()
        self.link_components()

    def setup_window(self):
        self.root.title("Student Management System")
        self.root.geometry("1200x500")
        self.root.configure(bg=self.theme["bg_color"])

        main_title = tk.Label(
            self.root,
            text="Student Management System (UOBS)",
            font=("Arial", 18, "bold"),
            fg=self.theme["frame_color"],
            bg=self.theme["success_color"],
            bd=2,
            pady=10,
        )
        main_title.pack(fill=tk.X)

    def create_widgets(self):
        self.left_frame = tk.Frame(
            self.root,
            bg=self.theme["frame_color"],
            padx=10,
            pady=10,
            relief=tk.RAISED,
            bd=2,
        )
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.right_frame = tk.Frame(
            self.root, bg=self.theme["bg_color"], relief=tk.RAISED, bd=2
        )
        self.right_frame.pack(
            side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10
        )

        self.form = StudentForm(self.left_frame, self.db_manager)
        self.table = StudentTableView(self.right_frame, self.db_manager)

    def link_components(self):
        self.table.set_form_callback(self.form_callback)

    def form_callback(self, values):
        fields = [
            "Registration#",
            "Student Name",
            "Email",
            "Contact#",
            "D.O.B",
            "Hostelite",
        ]
        for field, value in zip(fields, values):
            if field == "D.O.B":
                try:
                    date_obj = datetime.strptime(value, "%Y-%m-%d")
                    self.form.entries[field].set_date(date_obj)
                except ValueError:
                    pass
            else:
                if field == "Hostelite":
                    self.form.entries[field].set(value)
                else:
                    self.form.entries[field].delete(0, tk.END)
                    self.form.entries[field].insert(0, value)
