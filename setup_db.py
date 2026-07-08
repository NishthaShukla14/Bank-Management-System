import sqlite3

def setup_database():
    # Database se connect karna (bank.db file se)
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()

    # 1. Purani Users table ka setup (agar pehle se bani hai toh usko safe rakhega)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            balance REAL DEFAULT 0.0
        )
    ''')

    # 2. Yeh rahi humari Nayi Transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL,       -- Yahan aayega 'Deposit' ya 'Withdraw'
            status TEXT NOT NULL,     -- Yahan aayega 'Success' ya 'Pending'
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("BINGO! Database aur Transactions table ekdum ready hain!")

if __name__ == '__main__':
    setup_database()