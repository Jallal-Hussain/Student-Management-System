# ===== MAIN ===== #

import tkinter as tk
from models.database import DatabaseManager
from views.main_window import StudentManagementSystem


def main():
    root = tk.Tk()
    db_manager = DatabaseManager()

    # Create table if not exists
    db_manager.execute_query(
        """
        CREATE TABLE IF NOT EXISTS students (
            RegistrationNo VARCHAR(20) PRIMARY KEY,
            Name VARCHAR(50) NOT NULL,
            Email VARCHAR(50),
            Contact VARCHAR(15),
            DOB DATE,
            Hostelite VARCHAR(5)
        )
    """
    )

    app = StudentManagementSystem(root, db_manager)
    root.mainloop()
    app.db_manager.close_connection()


if __name__ == "__main__":
    main()
