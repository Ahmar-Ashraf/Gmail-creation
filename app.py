from flask import Flask, request, jsonify, render_template
import subprocess
import threading
import csv
import logging
import os

app = Flask(__name__)
ACCOUNTS_FILE = "created_accounts.csv"

logging.basicConfig(level=logging.INFO)

# Function to run the Gmail automation script
def run_gmail_script(num_accounts):
    try:
        subprocess.Popen(["python3", "gmail_script.py", str(num_accounts)])
        logging.info(f"Automation started for {num_accounts} accounts")
    except Exception as e:
        logging.error(f"Error starting automation: {e}")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/create_accounts", methods=["POST"])
def create_accounts():
    data = request.json
    num_accounts = data.get("num_accounts", 1)

    threading.Thread(target=run_gmail_script, args=(num_accounts,), daemon=True).start()
    return jsonify({"status": "success", "message": "Account creation started"}), 200

@app.route("/get_accounts")
def get_accounts():
    accounts = []
    if os.path.exists(ACCOUNTS_FILE):
        try:
            with open(ACCOUNTS_FILE, newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    accounts.append(row)
        except Exception as e:
            logging.error(f"Error reading accounts file: {e}")
    return jsonify(accounts)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)