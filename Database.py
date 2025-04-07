import json
import os
from random import randint
'''
# Path to the JSON file where item history is saved
item_history_file = "item_history.json"

def load_item_history():
    """Load item history from the JSON file."""
    if os.path.exists(item_history_file):
        with open(item_history_file, "r") as file:
            return json.load(file)
    else:
        print("No history file found.")
        return []

# Load the item history from the JSON file
item_history = load_item_history()

# Print all items from the history
if item_history:
    print("\nAccessing item history:")
    for item_data in item_history:
        print(f"Item: {item_data['label']}, ID: {item_data['id']}")
else:
    print("No items detected yet.")

def find_item_by_id(item_id):
    for item in item_history:
        if item["id"] == item_id:
            return item
    return None

# Find an item by its ID
item_id_to_search = input("Please enter the id number of the item you want to look up: ")
found_item = find_item_by_id(item_id_to_search)

if found_item:
    print(f"Item found: {found_item}")
else:
    print(f"Item with ID {item_id_to_search} not found.")

def save_item_history(item_history):
    """Save the updated item history to the JSON file."""
    with open(item_history_file, "w") as file:
        json.dump(item_history, file, indent=4)

save_item_history(item_history)
'''

# Base class
class Item:
    def __init__(self, label, color, description = "No description provided", location = ""):
        self.id = self.generate_id()
        self.label = label
        self.color = color
        self.description = description
        self.location = location
        self.image = f"{self.id + "(1)"}.jpg"

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, i):
        self._id = i    

    def generate_id(self):
        return ''.join(str(randint(0, 9)) for _ in range(16))

    def to_dict(self):
        return {
            "id": self.id,
            "label": self.label,
            "color": self.color,
            "description": self.description,
            "image": self.image,
            "location": self.location

        }
    

# Subclasses
class WaterBottle(Item): pass
class CellPhone(Item): pass
class Wallet(Item): pass
class Keys(Item): pass
class Laptop(Item): pass
class Glasses(Item): pass
class Headphones(Item): pass
class Calculator(Item): pass
class Watch(Item): pass
class Mouse(Item): pass
class Backpack(Item): pass
class Handbag(Item): pass

# Mapping
item_classes = {
    "water bottle": WaterBottle,
    "cell phone": CellPhone,
    "wallet": Wallet,
    "keys": Keys,
    "laptop": Laptop,
    "glasses": Glasses,
    "headphones": Headphones,
    "calculator": Calculator,
    "watch": Watch,
    "mouse": Mouse,
    "backpack": Backpack,
    "handbag": Handbag
}

# File path
item_history_file = "item_history.json"

# File helpers
def load_item_history():
    if os.path.exists(item_history_file):
        with open(item_history_file, "r") as file:
            return json.load(file)
    return []

def save_item_history(history):
    with open(item_history_file, "w") as file:
        json.dump(history, file, indent=4)

# Main function
def inputData(label, color, description, location):
    label = label.lower()
    if label not in item_classes:
        raise ValueError(f"Unknown item label: {label}")

    item_class = item_classes[label]
    item_instance = item_class(label, color, description, location)

    itemID = item_instance.id

    # Load, append, and save
    item_history = load_item_history()
    item_history.append(item_instance.to_dict())
    save_item_history(item_history)
    return itemID



