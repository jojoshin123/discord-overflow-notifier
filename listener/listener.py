import requests
import time
import os
from dotenv import load_dotenv

def postToOutputChannel(auth, message, attachmentUrls):
    body = {
        "content": message + attachmentUrls
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

URL = "https://discord.com/api/v9/channels/" + TEST_CHANNEL_ID + "/messages"
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
    newMessageList = list(res.json())
    
    if lastMessageHash != hash(newMessageList[0]["content"]):
        print(f"  New message found: {newMessageList[0]["content"]}")
        newMessage = newMessageList[0]
        
        # Attach attachments if any exist
        attachmentUrlString = ""
        for attachment in newMessage["attachments"]:
            attachmentUrlString += attachment["url"] + " "
        messageList = newMessageList
        lastMessageHash = hash(messageList[0]["content"])
        postToOutputChannel(auth, newMessage["content"], attachmentUrlString)
    else:
        print("  No new messages found")
        
    time.sleep(10)
    



