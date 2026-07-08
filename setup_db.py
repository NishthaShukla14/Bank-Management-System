import sqlite3

# Database se connect kar rahe hain
conn = sqlite3.connect('bank.db')
cursor = conn.cursor()

# Purane tables ko delete kar rahe hain taaki naya structure fresh ban sake
cursor.execute('DROP TABLE IF EXISTS Transactions')
cursor.execute('DROP TABLE IF EXISTS Accounts')
cursor.execute('DROP TABLE IF EXISTS Users')

# 1. Users Table
cursor.execute('''
CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# 2. Accounts Table
cursor.execute('''
CREATE TABLE Accounts (
    account_number INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    balance REAL DEFAULT 0.0,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
)
''')

# 3. Transactions Table (NAYA FEATURE)
# Ye table har deposit aur withdraw ka record rakhegi
cursor.execute('''
CREATE TABLE Transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    type TEXT NOT NULL, 
    amount REAL NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
)
''')

# 4. Dummy Data Insert kar rahe hain
cursor.execute('''
INSERT INTO Users (full_name, email, password)
VALUES ('Nishtha Shukla', 'nishtha@bank.com', '12345')
''')
user_id = cursor.lastrowid

# Account banaya aur Rs. 5000 dale
cursor.execute('INSERT INTO Accounts (user_id, balance) VALUES (?, 5000.0)', (user_id,))

# Pehli opening transaction ko passbook me likh diya
cursor.execute("INSERT INTO Transactions (user_id, type, amount) VALUES (?, 'Deposit', 5000.0)", (user_id,))

conn.commit()
conn.close()

print("BINGO! Database Upgraded! Transactions table successfully add ho gayi hai.")