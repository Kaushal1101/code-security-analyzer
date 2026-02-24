import os
import subprocess
import hashlib
import pickle
from flask import Flask, request
import sqlite3

app = Flask(__name__)

# --- 1. Hardcoded Secret ---
SECRET_KEY = "supersecret123"

# --- 2. Weak Cryptography ---
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

# --- 3. SQL Injection ---
def get_user(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = %s" % user_id
    cursor.execute(query)
    return cursor.fetchall()

# --- 4. Command Injection ---
def delete_file(filename):
    subprocess.call("rm -rf " + filename, shell=True)

# --- 5. Unsafe Deserialization ---
def load_user_data(data):
    return pickle.loads(data)

# --- 6. Dangerous eval ---
@app.route("/calculate")
def calculate():
    expression = request.args.get("expr")
    return str(eval(expression))

# --- 7. Debug Mode Enabled ---
if __name__ == "__main__":
    app.run(debug=True)

