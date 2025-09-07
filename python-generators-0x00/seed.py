import sqlite3
import csv

def connect_db():
    try:
        connection = sqlite3.connect('ALX_prodev.db')
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def create_database(connection):
    pass  # SQLite creates database automatically

def connect_to_prodev():
    return connect_db()

def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                age REAL NOT NULL
            )
        """)
        cursor.close()
    except Exception as e:
        print(f"Error creating table: {e}")

def insert_data(connection, csv_file):
    try:
        cursor = connection.cursor()
        with open(csv_file, 'r') as file:
            csv_reader = csv.DictReader(file)
            for i, row in enumerate(csv_reader, 1):
                cursor.execute(
                    "INSERT OR IGNORE INTO user_data (user_id, name, email, age) VALUES (?, ?, ?, ?)",
                    (f"user_{i}", row['name'], row['email'], row['age'])
                )
        connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error inserting data: {e}")

if __name__ == "__main__":
    connection = connect_db()
    if connection:
        create_database(connection)
        connection.close()
        print("Connection successful")

        connection = connect_to_prodev()
        if connection:
            create_table(connection)
            insert_data(connection, 'user_data.csv')
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_data'")
            result = cursor.fetchone()
            if result:
                print("Database ALX_prodev is present")
            cursor.execute("SELECT * FROM user_data LIMIT 5")
            rows = cursor.fetchall()
            print(rows)
            cursor.close()
            connection.close()