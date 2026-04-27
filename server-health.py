import subprocess

import os

def get_info(command_text):
    try:
        result = subprocess.run(command_text.split(), capture_output=True, text=True)
        return result.stdout
    except FileNotFoundError:
        # If the command doesn't exist (like 'free' on Mac), return a nice message
        return f"Command '{command_text}' not found on this OS."

print("Gathering data...")
name   = get_info("hostname")
time   = get_info("uptime")
disk   = get_info("df -h")
memory = get_info("free -h")
ports  = get_info("ss -tuln")

report = f"""
SERVER HEALTH REPORT
====================
HOSTNAME: {name}
UPTIME:   {time}

DISK SPACE:
{disk}

MEMORY:
{memory}

LISTENING PORTS:
{ports}
"""
os.makedirs("/Users/achore/Desktop/tufin-training/bash/tufin-training-exercise/tufin-lab/logs", exist_ok=True)

file_path = "/Users/achore/Desktop/tufin-training/bash/tufin-training-exercise/tufin-lab/logs/health-report.txt"
with open(file_path, "w") as file:
    file.write(report)

print(f"Done! Report saved to {file_path}")
