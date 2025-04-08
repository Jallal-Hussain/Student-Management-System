# ===== DATABASE MANAGER CLASS ===== #

import mysql.connector
from mysql.connector import Error
import configparser
import os
import tkinter.messagebox as messagebox


class DatabaseManager:
    """Handles MySQL database operations with configurable credentials."""

    def __init__(self, config_file="config.ini"):
        self.config_file = config_file
        self.load_config()
        self.connection = self.create_connection()

    def load_config(self):
        self.config = configparser.ConfigParser(interpolation=None)

        if not os.path.exists(self.config_file):
            self.config["DATABASE"] = {
                "host": "localhost",
                "user": "root",
                "password": "password",
                "database": "uobs",
            }
            with open(self.config_file, "w") as configfile:
                self.config.write(configfile)
            messagebox.showinfo(
                "Info", f"Created default config file at {self.config_file}"
            )

        self.config.read(self.config_file)
        db_config = self.config["DATABASE"]
        self.host = db_config.get("host", "localhost")
        self.user = db_config.get("user", "root")
        self.password = db_config.get("password", "password")
        self.database = db_config.get("database", "uobs")

    def create_connection(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                passwd=self.password,
                database=self.database,
            )
            print("Connected to MySQL Database successfully")
            return connection
        except Error as e:
            print(f"Database Connection Error: {e}")
            try:
                connection = mysql.connector.connect(
                    host=self.host, user=self.user, passwd=self.password
                )
                cursor = connection.cursor()
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
                cursor.close()
                connection.close()

                connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    passwd=self.password,
                    database=self.database,
                )
                return connection
            except Error as e:
                print(f"Database Creation Error: {e}")
                return None

    def execute_query(self, query, data=None):
        if self.connection:
            cursor = self.connection.cursor()
            try:
                if data:
                    cursor.execute(query, data)
                else:
                    cursor.execute(query)
                self.connection.commit()
                return True
            except Error as e:
                print(f"Error executing query: {e}")
                return False
            finally:
                cursor.close()
        return False

    def fetch_all(self, query, data=None):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, data) if data else cursor.execute(query)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error fetching data: {err}")
            return None
        finally:
            cursor.close()

    def fetch_one(self, query, data=None):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, data) if data else cursor.execute(query)
            return cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error fetching data: {err}")
            return None
        finally:
            cursor.close()

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Connection closed successfully")
