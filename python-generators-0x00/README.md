# Python Generators 0x00: SQLite User Data Example

This project demonstrates basic usage of SQLite in Python for storing and querying user data. It includes scripts to create a database, seed it with data from a CSV file, and query the database for specific users.

## Project Structure

- `seed.py`: Creates the SQLite database (`ALX_prodev.db`), defines the `user_data` table, and populates it with data from `user_data.csv`.
- `query_db.py`: Connects to the database and queries for users named 'Alice', printing the results.
- `user_data.csv`: Sample user data (name, email, age) used to populate the database.
- `ALX_prodev.db`: The generated SQLite database file.
- `requirements.txt`: Lists required Python packages (note: only `sqlite3` is used in the scripts, which is included in Python's standard library).

## Setup & Usage

1. **Install Python 3** (if not already installed).
2. (Optional) Create a virtual environment:
	```powershell
	python -m venv venv
	.\venv\Scripts\activate
	```
3. **Install dependencies** (not strictly required for SQLite):
	```powershell
	pip install -r requirements.txt
	```
4. **Seed the database:**
	```powershell
	python seed.py
	```
5. **Query the database:**
	```powershell
	python query_db.py
	```

## Example Output

```
Tables: [('user_data',)]
(user_1, 'Alice', 'alice@example.com', 30)
```

## Notes

- The scripts use SQLite, so no external database server is required.
- The `requirements.txt` lists `mysql-connector-python`, but it is not used in the current scripts.
- You can modify `user_data.csv` to add more users.

---
*Project for ALX Backend Python*
