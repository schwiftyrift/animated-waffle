import json
import os
from random import randint
import difflib
import spacy
nlp = spacy.load("en_core_web_md")

# Base class
class Item:
    def __init__(self, label, color, secondImage, date, description = "No description provided", location = ""):
        self.id = self.generate_id()
        self.date = date
        self.label = label
        self.color = color
        self.description = description
        self.location = location
        self.image = f"images/{self.id}(1).jpg"
        if secondImage:
            self.secondImage = f"images/{self.id}(2).jpg"
        else:
            self.secondImage = "None"


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
            "date": self.date,
            "description": self.description,
            "image": self.image,
            "secondImage": self.secondImage,
            "location": self.location,
            "status": "available",
            "claimed_by": "",
            "checkedOutTo": ""

        }
    

# Subclasses
class Bottle(Item): pass
class CellPhone(Item): pass
class Wallet(Item): pass
class Keys(Item): pass
class Laptop(Item): pass
class Sunglasses(Item): pass
class Headphones(Item): pass
class Calculator(Item): pass
class Watch(Item): pass
class Mouse(Item): pass
class Backpack(Item): pass
class Handbag(Item): pass

# Mapping
item_classes = {
    "bottle": Bottle,
    "cell phone": CellPhone,
    "wallet": Wallet,
    "keys": Keys,
    "laptop": Laptop,
    "sunglasses": Sunglasses,
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
def inputData(label, color, secondImage, date, description, location):
    label = label.lower()
    if label not in item_classes:
        raise ValueError(f"Unknown item label: {label}")

    item_class = item_classes[label]
    item_instance = item_class(label, color, secondImage, date, description, location)

    itemID = item_instance.id

    # Load, append, and save
    item_history = load_item_history()
    item_history.append(item_instance.to_dict())
    save_item_history(item_history)
    return itemID

def checkout_item(item_id):
    item_history = load_item_history()
    updated = False

    for item in item_history:
        if item["id"] == item_id and item["status"] == "available":
            item["status"] = "checked-out"
            item["checkedOutTo"] = item["claimed_by"]
            item["claimed_by"] = ""
            updated = True
            break

    if updated:
        save_item_history(item_history)
        return True
    else:
        return False  # item not found or already checked out

def lookup_item_by_id(item_id):
    item_history = load_item_history()
    for item in item_history:
        if item["id"] == item_id:
            return item
    return None

def get_closest_label_spacy(query, labels, threshold=0.75):
    query_doc = nlp(query.lower())
    best_label = None
    best_score = 0

    for label in labels:
        label_doc = nlp(label.lower())
        similarity = query_doc.similarity(label_doc)
        if similarity > best_score and similarity >= threshold:
            best_score = similarity
            best_label = label

    return best_label

def search_items_by_label(query, cutoff=0.6):
    query = query.strip().lower()
    item_history = load_item_history()
    results = []

    # Step 1: Fuzzy Match
    for item in item_history:
        if item["status"] != "available":
            continue
        label = item["label"].lower()
        score = difflib.SequenceMatcher(None, query, label).ratio()
        if score >= cutoff:
            results.append({
                "id": item["id"],
                "label": item["label"],
                "color": item["color"],
                "date": item["date"],
                "description": item["description"],
                "location": item["location"],
                "image": item["image"],
                "secondImage": item["secondImage"]
            })

    # Step 2: If nothing found, try semantic match using spaCy
    if not results:
        labels = set(item["label"] for item in item_history)
        closest_label = get_closest_label_spacy(query, labels)

        if closest_label:
            for item in item_history:
                if item["label"].lower() == closest_label.lower() and item["status"] == "available":
                    results.append({
                        "id": item["id"],
                        "label": item["label"],
                        "color": item["color"],
                        "description": item["description"],
                        "location": item["location"],
                        "image": item["image"],
                        "secondImage": item["secondImage"]
                    })

    return results

def claim_item(item_id, cwid):
    item_history = load_item_history()
    updated = False

    for item in item_history:
        if item["id"] == item_id and item["status"] == "available":
            item["claimed_by"] = cwid
            updated = True
            break

    if updated:
        save_item_history(item_history)
        return True
    else:
        return False  # Item not available to claim
    
def lookup_items_by_claim(cwid):
    item_history = load_item_history()
    claimed_items = []

    for item in item_history:
        if item.get("claimed_by") == cwid:
            claimed_items.append(item)

    return claimed_items

def clear_claimed(item_id):
    item_history = load_item_history()
    updated = False

    for item in item_history:
        if item["id"] == item_id and item["status"] == "available":
            item["checkedOutTo"] = ""
            item["claimed_by"] = ""
            updated = True
            break

    if updated:
        save_item_history(item_history)
        return True