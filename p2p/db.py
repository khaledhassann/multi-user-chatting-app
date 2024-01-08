from pymongo import MongoClient
import random


# mongoPass = tJgmWD36mFJoAWHm
# Includes database operations
class DB:


    # db initializations
    def __init__(self):
        self.client = MongoClient('mongodb+srv://johnwadie:john123654@cluster0.okxf27l.mongodb.net/')
        self.db = self.client['p2p-chat']


    # checks if the port number is already in use by another online user
    # def generate_unique_port(self):
    #     while True:
    #         # Generate a random port number
    #         port = random.randint(1024, 49151)

    #         # Check if the port exists in the "online_peers" collection
    #         existing_port = self.db.online_peers.find_one({'port': port})

    #         if not existing_port:
    #             # If the port is not found, return the unique port
    #             return port
        
    def isPortInUse(self, portNum):
        count = self.db.online_peers.count_documents({'port': portNum})
        return count > 0
    
    # Function to display the list of all usernames of online users
    def display_online_usernames(self):
        online_users = self.db.online_peers.find({}, {"_id": 0, "username": 1})
        usernames = [user["username"] for user in online_users]
        print("Online Usernames:")
        for username in usernames:
            print(username)

    # checks if an account with the username exists
    def is_account_exist(self, username):
        count = self.db.accounts.count_documents({'username': username})
        return count > 0
    

    # registers a user 
    def register(self, username, password):
        account = {
            "username": username,
            "password": password
        }
        self.db.accounts.insert_one(account)


    # retrieves the password for a given username
    def get_password(self, username):
        return self.db.accounts.find_one({"username": username})["password"]


    # checks if an account with the username online
    def is_account_online(self, username):
        if self.db.online_peers.count_documents({"username": username}) > 0:
            return True
        else:
            return False

    
    # logs in the user
    def user_login(self, username, ip, port):
        online_peer = {
            "username": username,
            "ip": ip,
            "port": port
        }
        self.db.online_peers.insert_one(online_peer)
    

    # logs out the user 
    def user_logout(self, username):
        self.db.online_peers.delete_one({"username": username})
    

    # retrieves the ip address and the port number of the username
    def get_peer_ip_port(self, username):
        res = self.db.online_peers.find_one({"username": username})
        return (res["ip"], res["port"])
    
    # New: display list of chat rooms
    def display_available_chat_rooms(self):
        # Retrieve available chat rooms
        available_rooms = self.db.chat_rooms.find()
        print("Available Chat Rooms:")
        for room in available_rooms:
            print(f"- {room['name']}")

    # New: Check if a chat room exists
    def is_chat_room_exist(self, room_name):
        count = self.db.chat_rooms.count_documents({'name': room_name})
        return count > 0

    # New: Create a chat room
    def create_chat_room(self, room_name):
        chat_room = {
            "name": room_name,
            "participants": [],
            "messages": []
        }
        self.db.chat_rooms.insert_one(chat_room)

    # New: Join a chat room
    def join_chat_room(self, username, room_name):
        self.db.chat_rooms.update_one(
            {"name": room_name},
            {"$push": {"participants": username}}
        )

    # New: Get chat room participants
    def get_chat_room_participants(self, room_name):
        participants = self.db.chat_rooms.find_one({"name": room_name}, {"_id": 0, "participants": 1})
        return participants.get("participants", [])

    # New: Add a message to a chat room
    def add_chat_room_message(self, room_name, sender, message):
        self.db.chat_rooms.update_one(
            {"name": room_name},
            {"$push": {"messages": {"sender": sender, "message": message}}}
        )

    # New: Get chat room messages
    def get_chat_room_messages(self, room_name):
        messages = self.db.chat_rooms.find_one({"name": room_name}, {"_id": 0, "messages": 1})
        return messages.get("messages", [])
