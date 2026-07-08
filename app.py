from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'super_secret_bank_key'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_email = request.form.get('email')
        user_password = request.form.get('password')
        
        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE email = ? AND password = ?", (user_email, user_password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            return redirect('/dashboard')
        else:
            return f"<h1 style='color: #ff4757; text-align: center; margin-top: 50px; font-family: sans-serif;'>Error: Invalid Email or Password! ❌</h1>"
            
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
        
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    
    # 1. Balance fetch karo
    cursor.execute("SELECT balance FROM Accounts WHERE user_id = ?", (session['user_id'],))
    account = cursor.fetchone()
    current_balance = account[0] if account else 0.0
    
    # 2. Transaction history fetch karo (Latest 5 transactions)
    cursor.execute("SELECT type, amount, date FROM Transactions WHERE user_id = ? ORDER BY date DESC LIMIT 5", (session['user_id'],))
    transactions = cursor.fetchall()
    conn.close()
    
    return render_template('dashboard.html', user_name=session['user_name'], balance=current_balance, transactions=transactions)

@app.route('/deposit', methods=['POST'])
def deposit():
    if 'user_id' not in session:
        return redirect('/')
        
    amount = float(request.form.get('amount'))
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    
    # Balance update karo aur Transaction history me likho
    cursor.execute("UPDATE Accounts SET balance = balance + ? WHERE user_id = ?", (amount, session['user_id']))
    cursor.execute("INSERT INTO Transactions (user_id, type, amount) VALUES (?, 'Deposit', ?)", (session['user_id'], amount))
    
    conn.commit()
    conn.close()
    return redirect('/dashboard')

@app.route('/withdraw', methods=['POST'])
def withdraw():
    if 'user_id' not in session:
        return redirect('/')
        
    amount = float(request.form.get('amount'))
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT balance FROM Accounts WHERE user_id = ?", (session['user_id'],))
    current_balance = cursor.fetchone()[0]
    
    # Agar balance kafi hai, tabhi withdraw karo aur history me likho
    if current_balance >= amount:
        cursor.execute("UPDATE Accounts SET balance = balance - ? WHERE user_id = ?", (amount, session['user_id']))
        cursor.execute("INSERT INTO Transactions (user_id, type, amount) VALUES (?, 'Withdraw', ?)", (session['user_id'], amount))
        conn.commit()
    
    conn.close()
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)