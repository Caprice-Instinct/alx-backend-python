
import sqlite3

def stream_users_in_batches(batch_size):
	connection = sqlite3.connect('ALX_prodev.db')
	connection.row_factory = sqlite3.Row
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM user_data")
	batch = []
	for row in cursor:
		batch.append(dict(row))
		if len(batch) == batch_size:
			yield batch
			batch = []
	if batch:
		yield batch
	return
	cursor.close()
	connection.close()

def batch_processing(batch_size):
	for batch in stream_users_in_batches(batch_size):
		for user in batch:
			if user['age'] > 25:
				print(user)


if __name__ == "__main__":
	batch_processing(3)
