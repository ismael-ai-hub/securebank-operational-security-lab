<<<<<<< HEAD
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
import os
import json
import uuid
from datetime import datetime, UTC
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "logs", "auth.log")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
REPORT_FILE = os.path.join(REPORTS_DIR, "incident_report.json")

THRESHOLD = 5

def severity_from_count(count: int) -> str:
    if count >= 10:
        return "HIGH"
    if count >= 7:
        return "MEDIUM"
    return "LOW"

def analyze_logs():
    if not os.path.exists(LOG_FILE):
        print("Log file not found.")
        return

    os.makedirs(REPORTS_DIR, exist_ok=True)

    failed_by_user = defaultdict(int)
    failed_by_ip = defaultdict(int)

    timestamps = []

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if "FAILED_LOGIN" not in line:
                continue

            parts = [p.strip() for p in line.strip().split("|")]

            # Extract timestamp
            timestamp_str = parts[0]
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=UTC)
            timestamps.append(timestamp)

            user = None
            ip = None

            for p in parts:
                if p.startswith("user="):
                    user = p.split("=", 1)[1].strip()
                elif p.startswith("ip="):
                    ip = p.split("=", 1)[1].strip()

            if user:
                failed_by_user[user] += 1
            if ip:
                failed_by_ip[ip] += 1

    if not timestamps:
        print("No failed login attempts detected.")
        return

    first_seen = min(timestamps)
    last_seen = max(timestamps)
    duration_seconds = (last_seen - first_seen).total_seconds()

    alerts = []
    now = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

    for user, count in failed_by_user.items():
        if count >= THRESHOLD:
            alerts.append({
                "entity_type": "user",
                "entity": user,
                "failed_attempts": count,
                "severity": severity_from_count(count)
            })

    for ip, count in failed_by_ip.items():
        if count >= THRESHOLD:
            alerts.append({
                "entity_type": "ip",
                "entity": ip,
                "failed_attempts": count,
                "severity": severity_from_count(count)
            })

    if not alerts:
        print("No brute force pattern detected.")
        return

    for a in alerts:
        print(f"ALERT [{a['severity']}]: BRUTE_FORCE on {a['entity_type']}='{a['entity']}' ({a['failed_attempts']} failed attempts)")

    incident = {
        "incident_id": f"SB-{datetime.now(UTC).strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}",
        "type": "AUTH_BRUTE_FORCE",
        "severity": max(alerts, key=lambda x: severity_from_count(x["failed_attempts"]))["severity"],
        "status": "OPEN",
        "detected_at_utc": now,
        "timeline": {
            "first_seen": first_seen.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "last_seen": last_seen.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "duration_seconds": duration_seconds,
            "attempts_per_minute": round(len(timestamps) / max(duration_seconds / 60, 1), 2)
        },
        "total_failed_attempts": len(timestamps),
        "log_source": "logs/auth.log"
    }

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(incident, f, indent=2)

    print(f"\nIncident report generated: {REPORT_FILE}")

if __name__ == "__main__":
    analyze_logs()
 8cb1189 (Implement auth logging, SOC detection, and banking risk matrix)
