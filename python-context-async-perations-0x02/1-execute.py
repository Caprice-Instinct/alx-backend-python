# create a reusable context manager that takes a query as input and executes it, managing both connection and the query execution

# Implement a class based custom context manager ExecuteQuery that takes the query: "SELECT * FROM users WHERE age > ?" and the parameter 25 and returns the result of the query

# Ensure to use the__enter__() and the __exit__() methods

import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.connection = None
        self.result = None
    
    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        cursor = self.connection.cursor()
        cursor.execute(self.query, self.params)
        self.result = cursor.fetchall()
        return self.result
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()

# Use the context manager
with ExecuteQuery('users.db', "SELECT * FROM users WHERE age > ?", (25,)) as results:
    for row in results:
        print(row)