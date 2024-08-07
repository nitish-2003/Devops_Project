from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL database connection
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='your_username',
        password='your_password',
        database='your_database'
    )
    return connection

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Query to check if the user exists
    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    if user:
        return f"Welcome, {user['email']}!"
    else:
        error_message = "Invalid credentials!"
        return render_template('login.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
