import json
import os

# Path to store the admin password
ADMIN_JSON_PATH = "data/admin_password.json"

def load_admin_password():
    """Load admin password from the JSON file."""
    if not os.path.exists(ADMIN_JSON_PATH):
        return None
    with open(ADMIN_JSON_PATH, 'r') as file:
        return json.load(file)

def save_admin_password(new_password):
    """Save a new admin password into the JSON file."""
    with open(ADMIN_JSON_PATH, 'w') as file:
        json.dump({"password": new_password}, file)
