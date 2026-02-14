 HEAD
from flask import Flask, request, jsonify
import os
import datetime

app = Flask(__name__)

USERS = {
    "admin": "SecurePass123",
    "analyst": "RiskMonitor2026"
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "logs", "auth.log")

def log_event(event_type, username, ip):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} | {event_type} | user={username} | ip={ip}\n"

    with open(LOG_FILE, "a") as f:
        f.write(log_entry)

@app.route("/")
def home():
    return "SecureBank Operational Security Lab"

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    ip_address = request.remote_addr

    if USERS.get(username) == password:
        log_event("SUCCESS_LOGIN", username, ip_address)
        return jsonify({"message": "Login successful"}), 200
    else:
        log_event("FAILED_LOGIN", username, ip_address)
        return jsonify({"message": "Login failed"}), 401

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, jsonify
import os
import datetime

app = Flask(__name__)

USERS = {
    "admin": "SecurePass123",
    "analyst": "RiskMonitor2026"
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "logs", "auth.log")

def log_event(event_type, username, ip):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} | {event_type} | user={username} | ip={ip}\n"

    with open(LOG_FILE, "a") as f:
        f.write(log_entry)

@app.route("/")
def home():
    return "SecureBank Operational Security Lab"

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    ip_address = request.remote_addr

    if USERS.get(username) == password:
        log_event("SUCCESS_LOGIN", username, ip_address)
        return jsonify({"message": "Login successful"}), 200
    else:
        log_event("FAILED_LOGIN", username, ip_address)
        return jsonify({"message": "Login failed"}), 401

if __name__ == "__main__":
    print("Starting SecureBank App...")
    app.run(host="127.0.0.1", port=5000, debug=True)
 8cb1189 (Implement auth logging, SOC detection, and banking risk matrix)
