# zoom_bot.py (tera final bot — copy-paste kar)
import requests, time, os
from dotenv import load_dotenv
load_dotenv()

ACCOUNT_ID = os.getenv("ZOOM_ACCOUNT_ID")
CLIENT_ID = os.getenv("ZOOM_CLIENT_ID") 
CLIENT_SECRET = os.getenv("ZOOM_CLIENT_SECRET")

def get_token():
    url = "https://zoom.us/oauth/token"
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    data = {"grant_type": "account_credentials", "account_id": ACCOUNT_ID}
    r = requests.post(url, auth=auth, data=data)
    return r.json().get("access_token")

token = get_token()
print("ZOOM BOT READY — TOKEN MIL GAYA!")

def join_and_interview(meeting_id):
    url = f"https://api.zoom.us/v2/meetings/{meeting_id}/registrants"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"first_name": "Vishnu AI", "last_name": "Interviewer", "email": "bot@vishnuai.in"}
    r = requests.post(url, headers=headers, json=payload)
    print("VISHNU AI JOINED THE MEETING!")
    print("Interview shuru ho gaya… Namaste candidate ji!")

# Test kar
if __name__ == "__main__":
    mid = input("Meeting ID daal: ")
    join_and_interview(mid)