import sqlite3

# Database se connect kar rahe hain
conn = sqlite3.connect('bank.db')
cursor = conn.cursor()

# Purane tables ko delete kar rahe hain taaki naya structure fresh ban sake
cursor.execute('DROP TABLE IF EXISTS Accounts')
cursor.execute('DROP TABLE IF EXISTS Users')

# 1. Users Table (User ki details ke liye)
cursor.execute('''
CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# 2. Accounts Table (User ke balance ke liye)
# Foreign Key use karke isko Users table se joda hai
cursor.execute('''
CREATE TABLE Accounts (
    account_number INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    balance REAL DEFAULT 0.0,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
)
''')

# 3. Dummy User insert kar rahe hain
cursor.execute('''
INSERT INTO Users (full_name, email, password)
VALUES ('Nishtha Shukla', 'nishtha@bank.com', '12345')
''')

# Jo user abhi insert hua, uski ID nikal rahe hain
user_id = cursor.lastrowid

# 4. Us user ke liye ek Account khol rahe hain jisme Rs. 5000 starting balance hai
cursor.execute('''
INSERT INTO Accounts (user_id, balance)
VALUES (?, 5000.0)
''', (user_id,))

# Changes ko save aur close kar rahe hain
conn.commit()
conn.close()

print("DATABASE UPGRADED SUCCESFULLY! Users aur Accounts dono tables ban gaye hain.")