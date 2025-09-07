if __name__ == "__main__":
    for i, page in enumerate(lazy_pagination(2)):
        print(f"Page {i+1}:")
        for user in page:
            print(user)
        if i == 1:
            break
import seed

def paginate_users(page_size, offset):
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    # Convert to list of dicts for consistency
    columns = [desc[0] for desc in cursor.description]
    result = [dict(zip(columns, row)) for row in rows]
    connection.close()
    return result

def lazy_pagination(page_size):
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
