import sqlite3

# 1. Database connection (Ye apne aap 'bank.db' naam ki ek nayi file bana dega)
conn = sqlite3.connect('bank.db')
cursor = conn.cursor()

# 2. Users table create karne ki SQL Query
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# 3. Ek default account insert karna taaki hum login test kar sakein
cursor.execute('''
INSERT OR IGNORE INTO Users (full_name, email, password)
VALUES ('Nishtha Shukla', 'nishtha@bank.com', '12345')
''')

# 4. Changes ko save karna aur connection close karna
conn.commit()
conn.close()

print("BINGO! Database (bank.db) aur Users table successfully ban gaya hai!")