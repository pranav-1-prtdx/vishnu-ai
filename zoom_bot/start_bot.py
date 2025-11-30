# zoom_bot/start_bot.py
import os
from zoom_bot import join_meeting_as_bot

# Ye meeting ID admin dashboard se aayega
MEETING_ID = input("Enter Zoom Meeting ID: ")
join_meeting_as_bot(MEETING_ID)
print("Bot deployed! Waiting for candidate...")