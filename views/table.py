# ===== Table View To Display Student Records ===== #

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from constants import THEME


class StudentTableView:
    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        self.theme = THEME
        self.create_search_controls()
        self.create_table_view()
        self.create_controls()

    def create_search_controls(self):
        search_frame = tk.Frame(self.parent, bg=self.theme["bg_color"], pady=10)
        search_frame.pack(fill=tk.X, padx=10)

        tk.Label(
            search_frame,
            text="Search By:",
            font=("Arial", 10, "bold"),
            fg=self.theme["text_color"],
            bg=self.theme["bg_color"],
        ).pack(side=tk.LEFT, padx=5)

        self.search_criteria = ttk.Combobox(
            search_frame,
            values=["Registration#", "Name", "Email", "Contact#", "D.O.B"],
            width=15,
            state="readonly",
        )
        self.search_criteria.pack(side=tk.LEFT, padx=5)
        self.search_criteria.current(0)

        self.search_entry = tk.Entry(
            search_frame, width=25, bg="#ECF0F1", fg="black", borderwidth=2
        )
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<Return>", lambda event: self.search_records())

        buttons = [
            ("Search", self.search_records, self.theme["button_color"]),
            ("Show All", self.refresh_table, self.theme["success_color"]),
            ("Clear Table", self.clear_table, self.theme["error_color"]),
        ]

        for text, command, color in buttons:
            tk.Button(
                search_frame,
                text=text,
                font=("Arial", 10, "bold"),
                width=10,
                bg=color,
                fg="white",
                command=command,
            ).pack(side=tk.LEFT, padx=5)

    def create_table_view(self):
        tree_frame = tk.Frame(self.parent, bg=self.theme["frame_color"])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        x_scroll = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        y_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("reg_no", "name", "email", "contact", "dob", "hostelite"),
            show="headings",
            xscrollcommand=x_scroll.set,
            yscrollcommand=y_scroll.set,
            selectmode="browse",
        )

        x_scroll.config(command=self.tree.xview)
        y_scroll.config(command=self.tree.yview)

        columns = [
            ("reg_no", "Registration#", 100, tk.CENTER),
            ("name", "Name", 150, tk.W),
            ("email", "Email", 150, tk.W),
            ("contact", "Contact#", 100, tk.CENTER),
            ("dob", "D.O.B", 100, tk.CENTER),
            ("hostelite", "Hostelite", 80, tk.CENTER),
        ]

        for col_id, heading, width, anchor in columns:
            self.tree.heading(col_id, text=heading)
            self.tree.column(col_id, width=width, anchor=anchor)

        style = ttk.Style()
        style.configure(
            "Treeview",
            background="#ECF0F1",
            fieldbackground="#ECF0F1",
            foreground="black",
        )
        style.configure(
            "Treeview.Heading",
            foreground=self.theme["frame_color"],
            font=("Arial", 10, "bold"),
        )

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def search_records(self):
        criteria = self.search_criteria.get()
        search_term = self.search_entry.get().strip()

        if not search_term:
            self.refresh_table()
            return

        criteria_map = {
            "Registration#": "RegistrationNo",
            "Name": "Name",
            "Email": "Email",
            "Contact#": "Contact",
            "D.O.B": "DOB",
        }

        db_column = criteria_map.get(criteria)
        if not db_column:
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        if criteria == "D.O.B":
            try:
                search_date = datetime.strptime(search_term, "%Y-%m-%d").date()
                query = f"SELECT * FROM students WHERE {db_column} = %s"
                params = (search_date,)
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
                return
        else:
            query = f"SELECT * FROM students WHERE {db_column} LIKE %s"
            params = (f"%{search_term}%",)

        records = self.db_manager.fetch_all(query, params)

        if records:
            for record in records:
                dob = record[4].strftime("%Y-%m-%d") if record[4] else ""
                self.tree.insert(
                    "",
                    tk.END,
                    values=(record[0], record[1], record[2], record[3], dob, record[5]),
                )
        else:
            messagebox.showinfo("Info", "No matching records found")

    def clear_table(self):
        if not messagebox.askyesno(
            "Confirm Clear",
            "Are you sure you want to delete ALL records?\nThis action cannot be undone!",
            icon="warning",
        ):
            return

        try:
            success = self.db_manager.execute_query("TRUNCATE TABLE students")
            if success:
                messagebox.showinfo("Success", "All records have been deleted")
                self.refresh_table()
            else:
                messagebox.showerror("Error", "Failed to clear the table")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item, "values")
            if hasattr(self, "form_callback"):
                self.form_callback(values)

    def create_controls(self):
        """Create additional control buttons."""
        control_frame = tk.Frame(self.parent, bg=self.theme["bg_color"], pady=10)
        control_frame.pack(fill=tk.X, padx=10)

        buttons = [
            ("Refresh", self.refresh_table, self.theme["info_color"]),
            ("Export CSV", self.export_to_csv, self.theme["success_color"]),
            ("Configure DB", self.configure_database, self.theme["warning_color"]),
        ]

        for text, command, color in buttons:
            button = tk.Button(
                control_frame,
                text=text,
                font=("Arial", 10, "bold"),
                width=12,
                bg=color,
                fg="white",
                command=command,
            )
            button.pack(side=tk.LEFT, padx=5)

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        query = (
            "SELECT RegistrationNo, Name, Email, Contact, DOB, Hostelite FROM students"
        )
        records = self.db_manager.fetch_all(query)

        if records:
            for record in records:
                dob = record[4].strftime("%Y-%m-%d") if record[4] else ""
                self.tree.insert(
                    "",
                    tk.END,
                    values=(record[0], record[1], record[2], record[3], dob, record[5]),
                )

    def export_to_csv(self):
        try:
            query = "SELECT * FROM students"
            records = self.db_manager.fetch_all(query)

            if not records:
                messagebox.showinfo("Info", "No records to export!")
                return

            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV Files", "*.csv")],
                title="Save Student Records",
            )

            if not file_path:
                return

            with open(file_path, "w") as f:
                f.write("RegistrationNo,Name,Email,Contact,DOB,Hostelite\n")

                for record in records:
                    dob = record[4].strftime("%Y-%m-%d") if record[4] else ""
                    line = f"{record[0]},{record[1]},{record[2]},{record[3]},{dob},{record[5]}\n"
                    f.write(line)

            messagebox.showinfo("Success", f"Records exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export records: {e}")

    def configure_database(self):
        """Open database configuration dialog."""
        config_dialog = tk.Toplevel(self.parent)
        config_dialog.title("Database Configuration")
        config_dialog.geometry("400x300")
        config_dialog.resizable(False, False)
        config_dialog.configure(bg=self.theme["frame_color"])

        # Load current config
        current_config = self.db_manager.config["DATABASE"]

        # Form fields
        fields = [
            ("Host", "host", current_config.get("host", "localhost")),
            ("Username", "user", current_config.get("user", "root")),
            ("Password", "password", current_config.get("password", "")),
            ("Database", "database", current_config.get("database", "uobs")),
        ]

        entries = {}
        for i, (label_text, field_name, default_value) in enumerate(fields):
            frame = tk.Frame(config_dialog, bg=self.theme["frame_color"])
            frame.pack(fill=tk.X, padx=10, pady=5)

            label = tk.Label(
                frame,
                text=label_text + ":",
                font=("Arial", 10),
                fg=self.theme["text_color"],
                bg=self.theme["frame_color"],
                width=12,
                anchor="w",
            )
            label.pack(side=tk.LEFT)

            entry = tk.Entry(frame, width=25, bg="#ECF0F1", fg="black", borderwidth=2)
            entry.insert(0, default_value)
            entry.pack(side=tk.LEFT, padx=5)
            entries[field_name] = entry

        # Buttons
        button_frame = tk.Frame(config_dialog, bg=self.theme["frame_color"], pady=10)
        button_frame.pack(fill=tk.X)

        def save_config():
            """Save the new configuration."""
            new_config = {
                "host": entries["host"].get(),
                "user": entries["user"].get(),
                "password": entries["password"].get(),
                "database": entries["database"].get(),
            }

            # Update config
            self.db_manager.config["DATABASE"] = new_config

            # Write to file
            with open(self.db_manager.config_file, "w") as configfile:
                self.db_manager.config.write(configfile)

            messagebox.showinfo(
                "Success",
                "Configuration saved successfully!\nPlease restart the application.",
            )
            config_dialog.destroy()

        save_button = tk.Button(
            button_frame,
            text="Save",
            font=("Arial", 10, "bold"),
            width=10,
            bg=self.theme["success_color"],
            fg="white",
            command=save_config,
        )
        save_button.pack(side=tk.LEFT, padx=10)

        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            font=("Arial", 10, "bold"),
            width=10,
            bg=self.theme["error_color"],
            fg="white",
            command=config_dialog.destroy,
        )
        cancel_button.pack(side=tk.LEFT, padx=10)

    def set_form_callback(self, callback):
        self.form_callback = callback
