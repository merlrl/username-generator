import random
import string
import re
from datetime import datetime

# Simulated storage (replace with Django models as needed)
USERNAME_HISTORY = []  # Each entry: {'id': int, 'username': str, 'favorite': bool, 'timestamp': str}
TAKEN_USERNAMES = set()  # Simulated set of usernames already taken
NEXT_ID = 1  # Auto-incrementing ID for history entries

def add_to_history(username):
    global NEXT_ID
    entry = {
        'id': NEXT_ID,
        'username': username,
        'favorite': False,
        'timestamp': datetime.now().isoformat()
    }
    USERNAME_HISTORY.append(entry)
    NEXT_ID += 1
    return entry

def generate_random_username(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def check_username_availability(username):
    return username not in TAKEN_USERNAMES

def generate_username_by_first_name(first_name):
    random_number = random.randint(100, 999)
    return f"{first_name}{random_number}"

def generate_username_from_phrase(phrase, unique=False):
    current_year = datetime.now().year
    # Insert underscore before uppercase letters (except the first letter)
    username_base = re.sub(r'(?<!^)(?=[A-Z])', '_', phrase)
    username = f"{username_base}{current_year}"
    if unique:
        username += str(random.randint(10, 99))
    return username

def generate_username_variation(username):
    variations = [
        username + str(random.randint(10, 99)),
        username.lower(),
        username.upper(),
        username[::-1],  # reversed username
        f"{username}_{random.randint(1, 9)}"
    ]
    available_variations = [u for u in variations if u not in TAKEN_USERNAMES]
    return available_variations

def filter_inappropriate_words(username, blacklist=None):
    if blacklist is None:
        blacklist = {"badword", "inappropriate"}
    filtered = username
    for word in blacklist:
        filtered = filtered.replace(word, '')
    return filtered

def check_username_complexity(username):
    has_letter = bool(re.search(r'[A-Za-z]', username))
    has_digit = bool(re.search(r'\d', username))
    has_symbol = bool(re.search(r'[!@#$%^&*]', username))
    return has_letter and has_digit and has_symbol

def validate_custom_username(username):
    valid_length = 6 <= len(username) <= 20
    has_letter = bool(re.search(r'[A-Za-z]', username))
    has_digit = bool(re.search(r'\d', username))
    return valid_length and has_letter and has_digit
