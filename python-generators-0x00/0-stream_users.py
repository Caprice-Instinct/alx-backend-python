
import sqlite3

def stream_users():
	connection = sqlite3.connect('ALX_prodev.db')
	connection.row_factory = sqlite3.Row  # To access columns by name
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM user_data")
	for row in cursor:
		yield dict(row)
	cursor.close()
	connection.close()



if __name__ == "__main__":
	from itertools import islice
	for user in islice(stream_users(), 6):
		print(user)