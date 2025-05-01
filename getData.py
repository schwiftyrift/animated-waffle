import json
import os

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