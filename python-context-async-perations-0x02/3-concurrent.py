#  Run multiple database queries concurrently using asyncio.gather.

# Use the aiosqlite library to interact with SQLite asynchronously. To learn more about it, click here.

# Write two asynchronous functions: async_fetch_users() and async_fetch_older_users() that fetches all users and users older than 40 respectively.

# Use the asyncio.gather() to execute both queries concurrently.

# Use asyncio.run(fetch_concurrently()) to run the concurrent fetch

import asyncio
import sqlite3

async def async_fetch_users():
    def fetch():
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()
        conn.close()
        return result
    return await asyncio.to_thread(fetch)

async def async_fetch_older_users():
    def fetch():
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE age > 40")
        result = cursor.fetchall()
        conn.close()
        return result
    return await asyncio.to_thread(fetch)

async def fetch_concurrently():
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("All users:", all_users)
    print("Older users:", older_users)

asyncio.run(fetch_concurrently())