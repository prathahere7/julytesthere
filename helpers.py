import sqlite3

def unsafe_query(user_input):
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE name = '{user_input}'"  # Unsafe!
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result
