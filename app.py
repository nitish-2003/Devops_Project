import os
from flask import Flask, render_template, request, redirect, url_for, jsonfy
import mysql.connector

app = Flask(__name__)

# Configure MySQL from environment variables
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'default_user')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'default_password')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'default_db')
# Initialize MySQL
mysql = MySQL(app)

def init_db():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
              id INT AUTO_INCREMENT PRIMARY KEY,
              email VARCHAR(255) NOT NULL UNIQUE,
              password VARCHAR(255) NOT NULL
        );
        ''')
        mysql.connection.commit()  
        cur.close()

# MySQL database connection
'''def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='your_username',
        password='your_password',
        database='your_database'
    )
    return connection
'''

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
