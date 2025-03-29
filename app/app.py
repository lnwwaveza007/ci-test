from flask import Flask, jsonify
import mysql.connector
import time
import os

app = Flask(__name__)

def create_db_connection():
    max_retries = 5
    retry_delay = 5  # seconds

    for attempt in range(max_retries):
        try:
            db = mysql.connector.connect(
                host="db",  # Use service name from docker-compose
                user="root",
                password="rootpassword",
                database="unidb"
            )
            return db
        except mysql.connector.Error as err:
            print(f"Connection attempt {attempt + 1} failed: {err}")
            time.sleep(retry_delay)
    
    raise Exception("Could not connect to database after multiple attempts")

@app.route('/')
def hello():
    return "Hello from Flask Backend!"

@app.route('/api/users')
def get_users():
    db = create_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM student")
    users = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
