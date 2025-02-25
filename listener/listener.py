import requests
import time
import os
from dotenv import load_dotenv

def postToOutputChannel(auth, message):
    body = {
        "content": message
    }
    res = requests.post(OUTPUT_URL,headers=auth, data=body)
    # TODO: Include hyperlink
    if res.status_code == 200:
        print("  Message posted to output channel")
    else:
        print(f"  Error posting message to output channel {res.text}")

load_dotenv()
TOKEN = os.getenv("TOKEN")
FOX_CHANNEL_ID = os.getenv("FOX_CHANNEL_ID")
TEST_CHANNEL_ID = os.getenv("TEST_CHANNEL_ID")
OUTPUT_CHANNEL_ID = os.getenv("OUTPUT_CHANNEL_ID")

URL = "https://discord.com/api/v9/channels/" + FOX_CHANNEL_ID + "/messages"
OUTPUT_URL = "https://discord.com/api/v9/channels/" + OUTPUT_CHANNEL_ID + "/messages"

auth = {
    "authorization": TOKEN
}

res = requests.get(URL,headers=auth)
messageList = [i["content"] for i in res.json()]

lastMessageHash = hash(messageList[0])

while True:
    print("Listening for new messages...")
    res = requests.get(URL,headers=auth)
    newMessageList = [i["content"] for i in res.json()]
    if lastMessageHash != hash(newMessageList[0]):
        print(f"  New message found: {newMessageList[0]}")
        messageList = newMessageList
        lastMessageHash = hash(messageList[0])
        postToOutputChannel(auth, newMessageList[0])
    else:
        print("  No new messages found")
        
    time.sleep(10)
    



