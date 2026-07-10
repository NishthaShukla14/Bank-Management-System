from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# To connect Database Shortcut function
def get_db():
    conn = sqlite3.connect('bank.db')
    return conn

# ==========================================
# 1. LOGIN ROUTE (index.html)
# ==========================================
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db()
        cursor = conn.cursor()
        # Database mein check karna ki user hai ya nahi
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (email, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['username'] = email  # Login successful
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password!', 'danger') # Galat password par error
            
    return render_template('index.html')

# ==========================================
# 2. SIGNUP ROUTE ( For Creating new account )
# ==========================================
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db()
        cursor = conn.cursor()
        try:
            # Naya user database mein daalna, shuruati balance 0.0
            cursor.execute("INSERT INTO users (username, password, balance) VALUES (?, ?, 0.0)", (email, password))
            conn.commit()
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Account with this email already exists!', 'danger')
        finally:
            conn.close()
            
    # Ek simple signup form bina alag HTML file banaye
    return '''
    <div style="font-family: Arial; text-align: center; margin-top: 50px;">
        <h2>Open New Account</h2>
        <form method="POST">
            <input type="email" name="email" placeholder="Enter Email" required style="padding: 10px; margin: 5px;"><br>
            <input type="password" name="password" placeholder="Enter Password" required style="padding: 10px; margin: 5px;"><br>
            <button type="submit" style="padding: 10px 20px; background: #2ed573; color: white; border: none; cursor: pointer;">Sign Up</button>
        </form>
        <br><a href="/">Back to Login</a>
    </div>
    '''

# ==========================================
# 3. DASHBOARD ROUTE (dashboard.html)
# ==========================================
@app.route('/dashboard')
def dashboard():
    # Agar bina login kiye koi dashboard kholne ki koshish kare
    if 'username' not in session:
        return redirect(url_for('login'))
        
    email = session['username']
    
    conn = get_db()
    cursor = conn.cursor()
    
    # User ka current balance nikalna
    cursor.execute("SELECT balance FROM users WHERE username=?", (email,))
    balance_row = cursor.fetchone()
    balance = balance_row[0] if balance_row else 0.0
    
    # User ke pichle transactions nikalna (sirf Deposit aur Withdraw dikhane ke liye)
    cursor.execute("SELECT type, amount, date FROM transactions WHERE username=? ORDER BY date DESC LIMIT 5", (email,))
    transactions = cursor.fetchall()
    conn.close()
    
    return render_template('dashboard.html', balance=balance, transactions=transactions)

# ==========================================
# 4. SMART TRANSFER ROUTE (Fraud Detection + Deposit/Withdraw Logic)
# ==========================================
@app.route('/transfer', methods=['POST'])
def transfer():
    if 'username' not in session:
        return redirect(url_for('login'))
        
    email = session['username']
    amount = float(request.form.get('amount', 0))
    transaction_type = request.form.get('type') # Form se aayega: 'Deposit' ya 'Withdraw'
    
    conn = get_db()
    cursor = conn.cursor()
    
    # --- BONUS LOGIC: Balance check before Withdraw ---
    if transaction_type == 'Withdraw':
        cursor.execute("SELECT balance FROM users WHERE username=?", (email,))
        current_balance = cursor.fetchone()[0]
        if amount > current_balance:
            flash('Failed: Insufficient Balance!', 'danger')
            conn.close()
            return redirect(url_for('dashboard'))

    status = 'Success'
    
    # --- FRAUD DETECTION LOGIC ---
    if amount > 50000:
        status = 'Pending'
        flash('Suspicious Activity: Approval needed for amounts over ₹50,000.', 'warning')
    else:
        # --- NORMAL BALANCE UPDATE ---
        if transaction_type == 'Deposit':
            cursor.execute("UPDATE users SET balance = balance + ? WHERE username=?", (amount, email))
        elif transaction_type == 'Withdraw':
            cursor.execute("UPDATE users SET balance = balance - ? WHERE username=?", (amount, email))
            
        flash(f'{transaction_type} of ₹{amount} was successful!', 'success')
        
    # --- SAVE TO TRANSACTION HISTORY ---
    cursor.execute("INSERT INTO transactions (username, amount, type, status) VALUES (?, ?, ?, ?)",
                   (email, amount, transaction_type, status))
    conn.commit()
    conn.close()
    
    return redirect(url_for('dashboard'))

# ==========================================
# 5. LOGOUT ROUTE
# ==========================================
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out securely.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
