import os

LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs", "auth.log")

THRESHOLD = 5  # Number of failed attempts before alert

def analyze_logs():
    if not os.path.exists(LOG_FILE):
        print("No log file found.")
        return

    failed_attempts = {}

    with open(LOG_FILE, "r") as f:
        lines = f.readlines()

    for line in lines:
        if "FAILED_LOGIN" in line:
            parts = line.strip().split("|")
            user_part = [p for p in parts if "user=" in p][0]
            user = user_part.split("=")[1].strip()

            failed_attempts[user] = failed_attempts.get(user, 0) + 1

    for user, count in failed_attempts.items():
        if count >= THRESHOLD:
            print(f"ALERT: Possible brute force attack detected for user '{user}' ({count} failed attempts)")

if __name__ == "__main__":
    analyze_logs()
