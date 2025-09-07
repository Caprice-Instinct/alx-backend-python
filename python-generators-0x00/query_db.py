import sqlite3

connection = sqlite3.connect('ALX_prodev.db')
cursor = connection.cursor()

# Show all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables:", tables)

# Show all data
cursor.execute("SELECT * FROM user_data WHERE name='Alice'")
rows = cursor.fetchall()
for row in rows:
    print(row)

connection.close()