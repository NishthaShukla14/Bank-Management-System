from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Form se user ka email aur password lena
        user_email = request.form.get('email')
        user_password = request.form.get('password')
        
        # 1. Database se connection banana
        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()
        
        # 2. SQL Query: Check karna ki kya ye email aur password table mein hain?
        cursor.execute("SELECT * FROM Users WHERE email = ? AND password = ?", (user_email, user_password))
        
        # 3. fetchone() se check karna ki result mila ya nahi
        user = cursor.fetchone() 
        conn.close() # Connection band kar diya
        
        # 4. Agar user mil gaya toh Success, warna Error
        if user:
            # user[1] ka matlab hai 'full_name' (Kyunki database mein 2nd number par naam hai)
            return f"<h1 style='color: #00d2ff; text-align: center; margin-top: 50px; font-family: sans-serif;'>Welcome {user[1]}! Login Successful! 🎉</h1>"
        else:
            return f"<h1 style='color: #ff4757; text-align: center; margin-top: 50px; font-family: sans-serif;'>Error: Invalid Email or Password! ❌</h1>"
            
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)