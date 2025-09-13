# create a class based context manager to handle opening and closing database connections automatically

# Write a class custom context manager DatabaseConnection using the __enter__ and the __exit__ methods

# Use the context manager with the with statement to be able to perform the query SELECT * FROM users. Print the results from the query.

import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
    
    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()

# Use the context manager
with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    for row in results:
        print(row)