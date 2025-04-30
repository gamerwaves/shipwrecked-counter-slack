import time
import requests
import subprocess
import json
from keep_alive import keep_alive
keep_alive()

# Webhook URL (replace with your actual Slack Incoming Webhook URL)
WEBHOOK_URL = "https://hooks.slack.com/services/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"

# URL to poll
API_URL = "https://shipwrecked.hackclub.com/api/stats/count"

# Initialize count
previous_count = None

def get_current_count():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json().get("count", 0)
    except Exception as e:
        print(f"Error fetching count: {e}")
        return None

def notify_slack(new_count, diff):
    # Create the message payload with the difference in count
    message = {
        "text": f"🎉 New Shipwrecked count: {new_count}\nDifference since last check: +{diff}"
    }
    
    # Send the message via curl to the Slack Webhook URL
    try:
        subprocess.run([
            "curl", "-X", "POST", 
            "-H", "Content-type: application/json", 
            "--data", json.dumps(message), 
            WEBHOOK_URL
        ])
        print("Slack message sent.")
    except Exception as e:
        print(f"Error sending message to Slack: {e}")

def main():
    global previous_count
    while True:
        current_count = get_current_count()
        if current_count is not None:
            if previous_count is not None and current_count > previous_count:
                # Calculate the difference
                diff = current_count - previous_count
                notify_slack(current_count, diff)
            previous_count = current_count
        time.sleep(60)  # Check every 60 seconds

if __name__ == "__main__":
    main()
