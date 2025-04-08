# ===== STUDENT FORM ===== #
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
from constants import THEME


class StudentForm:
    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        self.theme = THEME
        self.entries = {}
        self.create_form()

    def create_form(self):
        form_frame = tk.Frame(self.parent, bg=self.theme["frame_color"])
        form_frame.pack(fill=tk.X, pady=5)

        title_label = tk.Label(
            form_frame,
            text="Student Registration Form",
            font=("Arial", 14, "bold"),
            fg=self.theme["text_color"],
            bg=self.theme["frame_color"],
        )
        title_label.pack(pady=10)

        fields = [
            "Registration#",
            "Student Name",
            "Email",
            "Contact#",
            "D.O.B",
            "Hostelite",
        ]

        for field in fields:
            field_frame = tk.Frame(form_frame, bg=self.theme["frame_color"])
            field_frame.pack(fill=tk.X, pady=5)

            tk.Label(
                field_frame,
                text=field + ":",
                font=("Arial", 10, "bold"),
                fg=self.theme["text_color"],
                bg=self.theme["frame_color"],
                width=15,
                anchor="w",
            ).pack(side=tk.LEFT)

            if field == "D.O.B":
                entry = DateEntry(
                    field_frame,
                    width=27,
                    background="#1A5276",
                    foreground="white",
                    borderwidth=2,
                    date_pattern="yyyy-mm-dd",
                )
            elif field == "Hostelite":
                entry = ttk.Combobox(
                    field_frame, values=["Yes", "No"], width=27, state="readonly"
                )
            else:
                entry = tk.Entry(
                    field_frame, width=30, bg="#ECF0F1", fg="black", borderwidth=2
                )

            entry.pack(side=tk.LEFT, padx=5)
            self.entries[field] = entry

        button_frame = tk.Frame(form_frame, bg=self.theme["frame_color"], pady=10)
        button_frame.pack(fill=tk.X)

        buttons = [
            ("Add", self.add_student, self.theme["success_color"]),
            ("Update", self.update_student, self.theme["warning_color"]),
            ("Delete", self.delete_student, self.theme["error_color"]),
            ("Clear", self.clear_form, self.theme["other_color"]),
        ]

        for text, command, color in buttons:
            tk.Button(
                button_frame,
                text=text,
                font=("Arial", 10, "bold"),
                width=10,
                bg=color,
                fg="white",
                command=command,
            ).pack(side=tk.LEFT, padx=5, pady=5)

    def add_student(self):
        try:
            reg_no = self.entries["Registration#"].get().strip()
            name = self.entries["Student Name"].get().strip()
            email = self.entries["Email"].get().strip()
            contact = self.entries["Contact#"].get().strip()
            dob = self.entries["D.O.B"].get()
            hostelite = self.entries["Hostelite"].get()

            if not reg_no or not name:
                tk.messagebox.showwarning(
                    "Warning", "Registration# and Name are required!"
                )
                return

            check_query = (
                "SELECT RegistrationNo FROM students WHERE RegistrationNo = %s"
            )
            existing = self.db_manager.fetch_one(check_query, (reg_no,))
            if existing:
                tk.messagebox.showerror(
                    "Error", f"Registration# {reg_no} already exists!"
                )
                return

            dob_formatted = datetime.strptime(dob, "%Y-%m-%d").date() if dob else None
            data = (reg_no, name, email, contact, dob_formatted, hostelite)

            query = """
                INSERT INTO students 
                (RegistrationNo, Name, Email, Contact, DOB, Hostelite) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            success = self.db_manager.execute_query(query, data)

            if success:
                tk.messagebox.showinfo("Success", "Student record added successfully!")
            else:
                tk.messagebox.showerror("Error", "Failed to add student record.")
        except ValueError as ve:
            tk.messagebox.showerror("Error", f"Invalid date format: {ve}")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred: {e}")

    def update_student(self):
        try:
            reg_no = self.entries["Registration#"].get().strip()
            if not reg_no:
                tk.messagebox.showwarning(
                    "Warning", "Please select a record to update!"
                )
                return

            name = self.entries["Student Name"].get().strip()
            email = self.entries["Email"].get().strip()
            contact = self.entries["Contact#"].get().strip()
            dob = self.entries["D.O.B"].get()
            hostelite = self.entries["Hostelite"].get()

            if not name:
                tk.messagebox.showwarning("Warning", "Name is required!")
                return

            dob_formatted = datetime.strptime(dob, "%Y-%m-%d").date() if dob else None

            query = """
                UPDATE students 
                SET Name = %s, Email = %s, Contact = %s, DOB = %s, Hostelite = %s
                WHERE RegistrationNo = %s
            """
            data = (name, email, contact, dob_formatted, hostelite, reg_no)
            success = self.db_manager.execute_query(query, data)

            if success:
                tk.messagebox.showinfo(
                    "Success", "Student record updated successfully!"
                )
            else:
                tk.messagebox.showerror("Error", "Failed to update student record.")
        except ValueError as ve:
            tk.messagebox.showerror("Error", f"Invalid date format: {ve}")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred: {e}")

    def delete_student(self):
        reg_no = self.entries["Registration#"].get().strip()
        if not reg_no:
            tk.messagebox.showwarning("Warning", "Please select a record to delete!")
            return

        if not tk.messagebox.askyesno(
            "Confirm", "Are you sure you want to delete this record?"
        ):
            return

        query = "DELETE FROM students WHERE RegistrationNo = %s"
        success = self.db_manager.execute_query(query, (reg_no,))

        if success:
            tk.messagebox.showinfo("Success", "Student record deleted successfully!")
        else:
            tk.messagebox.showerror("Error", "Failed to delete student record.")

    def clear_form(self):
        for field, entry in self.entries.items():
            if field == "D.O.B":
                entry.set_date(datetime.now())
            elif field == "Hostelite":
                entry.set("")
            else:
                entry.delete(0, tk.END)
