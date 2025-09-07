import sqlite3

def stream_user_ages():
    connection = sqlite3.connect('ALX_prodev.db')
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:
        yield row[0]
    cursor.close()
    connection.close()

def average_user_age():
    total = 0
    count = 0
    for age in stream_user_ages():
        total += float(age)
        count += 1
    avg = total / count if count else 0
    print(f"Average age of users: {avg}")

if __name__ == "__main__":
    average_user_age()
