import sqlite3
import csv

def populate_users_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            age INTEGER
        )
    ''')
    
    with open('users.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            cursor.execute(
                'INSERT OR REPLACE INTO users (id, name, email, age) VALUES (?, ?, ?, ?)',
                (row['id'], row['name'], row['email'], row['age'])
            )
    
    conn.commit()
    conn.close()
    print("Database populated successfully!")

if __name__ == "__main__":
    populate_users_db()