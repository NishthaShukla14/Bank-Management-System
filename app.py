from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
# Session (login yaad rakhne) ke liye ek secret key zaroori hoti hai
app.secret_key = 'super_secret_bank_key'

# --- 1. LOGIN ROUTE ---
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
            # Login Success! User ki details session me save kar lo
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            return redirect('/dashboard') # Seedha dashboard par bhej do
        else:
            return f"<h1 style='color: #ff4757; text-align: center; margin-top: 50px; font-family: sans-serif;'>Error: Invalid Email or Password! ❌</h1>"
            
    return render_template('index.html')

# --- 2. DASHBOARD ROUTE ---
@app.route('/dashboard')
def dashboard():
    # Agar koi bina login kiye direct dashboard kholna chahe, toh usko wapas login pe bhejo
    if 'user_id' not in session:
        return redirect('/')
        
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    # Logged-in user ka balance fetch karo
    cursor.execute("SELECT balance FROM Accounts WHERE user_id = ?", (session['user_id'],))
    account = cursor.fetchone()
    conn.close()
    
    # Agar account hai toh balance lo, nahi toh 0.0 dikhao
    current_balance = account[0] if account else 0.0
    
    return render_template('dashboard.html', user_name=session['user_name'], balance=current_balance)

# --- 3. DEPOSIT ROUTE (Paise Jama Karna) ---
@app.route('/deposit', methods=['POST'])
def deposit():
    if 'user_id' not in session:
        return redirect('/')
        
    amount = float(request.form.get('amount'))
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    # SQL Update query se balance badhao
    cursor.execute("UPDATE Accounts SET balance = balance + ? WHERE user_id = ?", (amount, session['user_id']))
    conn.commit()
    conn.close()
    
    return redirect('/dashboard') # Update hone ke baad page refresh kar do

# --- 4. WITHDRAW ROUTE (Paise Nikalna) ---
@app.route('/withdraw', methods=['POST'])
def withdraw():
    if 'user_id' not in session:
        return redirect('/')
        
    amount = float(request.form.get('amount'))
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    
    # Pehle check karo ki account me utne paise hain bhi ya nahi
    cursor.execute("SELECT balance FROM Accounts WHERE user_id = ?", (session['user_id'],))
    current_balance = cursor.fetchone()[0]
    
    if current_balance >= amount:
        cursor.execute("UPDATE Accounts SET balance = balance - ? WHERE user_id = ?", (amount, session['user_id']))
        conn.commit()
    
    conn.close()
    return redirect('/dashboard')

# --- 5. LOGOUT ROUTE ---
@app.route('/logout')
def logout():
    session.clear() # User ka ID card (session) faad do
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)