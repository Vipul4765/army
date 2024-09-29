import json
import os
import logging

# Path to store the admin password
ADMIN_JSON_PATH = os.path.join("data", "admin_password.json")

logging.basicConfig(level=logging.INFO)


def load_admin_password():
    """Load admin password from the JSON file.

    Returns:
        str or None: The admin password if it exists; otherwise, None.
    """
    if not os.path.exists(ADMIN_JSON_PATH):
        logging.warning(f"Admin password file not found: {ADMIN_JSON_PATH}.")
        return None
    try:
        with open(ADMIN_JSON_PATH, 'r') as file:
            password_data = json.load(file)
            logging.info("Admin password loaded successfully.")
            return password_data.get("password")  # Return the password
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON from the admin password file.")
        return None
    except Exception as e:
        logging.error(f"An error occurred while loading the admin password: {e}")
        return None


def save_admin_password(new_password):
    """Save a new admin password into the JSON file.

    Args:
        new_password (str): The new password to save.
    """
    try:
        with open(ADMIN_JSON_PATH, 'w') as file:
            json.dump({"password": new_password}, file)
            logging.info("Admin password saved successfully.")
    except Exception as e:
        logging.error(f"An error occurred while saving the admin password: {e}")
