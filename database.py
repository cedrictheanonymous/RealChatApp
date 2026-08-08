import sqlite3

connection = sqlite3.connect("chat.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    message TEXT NOT NULL,
    time TEXT NOT NULL
)
""")

connection.commit()
connection.close()

print("Database created successfully!")
