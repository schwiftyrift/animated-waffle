import json
import os
from random import randint

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



