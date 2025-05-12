import json
import os
from random import randint

# File path for storing user credentials
user_data_file = "user_data.json"
notification_file = "notifications.json"

# File helpers to load and save user data
def load_user_data():
    if os.path.exists(user_data_file):
        with open(user_data_file, "r") as file:
            return json.load(file)
    return {}

def save_user_data(user_data):
    with open(user_data_file, "w") as file:
        json.dump(user_data, file, indent=4)


def load_notification():
    if os.path.exists(notification_file):
        with open(notification_file, "r") as file:
            return json.load(file)
    return []

# 1. User Registration: Prompt user to create a username and password
def register_user(username, password, name, userType):
    user_data = load_user_data()

    if username in user_data:
        #print("Username already exists. Please choose a different one.")
        return False

    user_data[username] = {
        "password": password,
        "name": name,
        "userType": userType
    }

    save_user_data(user_data)
    #print(f"User '{username}' registered successfully!")
    return True

# 2. Login Verification: Check if the provided username and password match
def login(username, password):
    user_data = load_user_data()

    if username in user_data and user_data[username]["password"] == password:
        #print(f"Welcome, {username}!")
        return True
    else:
        #print("Invalid username or password.")
        return False

# 3. Change Username (if user forgets or wants to update)
def change_username(old_username, new_username, password):
    user_data = load_user_data()

    if old_username in user_data and user_data[old_username] == password:
        if new_username in user_data:
            print("New username already taken.")
            return False
        user_data[new_username] = user_data.pop(old_username)
        save_user_data(user_data)
        print(f"Username changed successfully to {new_username}!")
        return True
    else:
        print("Old username or password is incorrect.")
        return False

# 4. Change Password (if user forgets or wants to update)
def change_password(username, old_password, new_password):
    user_data = load_user_data()

    if username in user_data and user_data[username]["password"] == old_password:  # Check if old password matches
        user_data[username]["password"] = new_password  # Update the password field
        save_user_data(user_data)  # Save the updated data back to storage
        return True  # Return True to indicate password change was successful
    else:
        return False  # Return False if username or old password is incorrect
    
def check_old_password(username, old_password):
    user_data = load_user_data()

    # Validate if the old password is correct
    if username in user_data and user_data[username]["password"] == old_password:
        return True
    return False

def isUser(username):
    user_data = load_user_data()

    if username not in user_data:
        return False

    return True

def isAdmin(username):
    user_data = load_user_data()
    return user_data.get(username, {}).get("userType") == "admin"

def createNotification(username, message, date):
    id = "".join(str(randint(0, 9)) for _ in range(16))
    notification_data = load_notification()
    
    notification_data[id] = {
        "recipient": username,
        "message": message,
        "date": date
        }
    
    with open("notifications.json", "w") as f:
        json.dump(notification_data, f, indent=4)


def retrieveNotifications(username):
    notification_history = load_notification()  # dict of notif_id: notif_data
    results = []

    for notif_id, notif in notification_history.items():
        if notif.get("recipient") == username:
            results.append({
                "id": notif_id,
                "message": notif.get("message"),
                "date": notif.get("date")
            })

    return results

def remove_notification(notification_id):
    with open("notifications.json", "r") as f:
        notifications = json.load(f)

    if notification_id in notifications:
        del notifications[notification_id]

        with open("notifications.json", "w") as f:
            json.dump(notifications, f, indent=4)


"""""""""
username = input("Enter a new username: ")
password = input("Enter a password: ")
register_user(username, password)

# Example: Login with a username and password
username = input("Enter your username: ")
password = input("Enter your password: ")
login(username, password)

# Example: Change username
old_username = input("Enter your old username: ")
new_username = input("Enter a new username: ")
password = input("Enter your current password: ")
change_username(old_username, new_username, password)

# Example: Change password
username = input("Enter your username: ")
old_password = input("Enter your old password: ")
new_password = input("Enter your new password: ")
change_password(username, old_password, new_password)"
"""""""""""
