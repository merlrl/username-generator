from django.http import JsonResponse
import random, string, json, re
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

# ---------------------------
# Global Variables for Simulation
# ---------------------------
USERNAME_HISTORY = []  # Each entry: {'id': int, 'username': str, 'favorite': bool, 'timestamp': datetime}
TAKEN_USERNAMES = set()  # Simulated taken usernames
NEXT_ID = 1  # For username history entries

def add_to_history(username):
    global NEXT_ID
    entry = {
        'id': NEXT_ID,
        'username': username,
        'favorite': False,
        'timestamp': datetime.now().isoformat()
    }
    USERNAME_HISTORY.append(entry)
    TAKEN_USERNAMES.add(username)  # Mark username as taken
    NEXT_ID += 1
    return entry


def generate_random_username(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# ---------------------------
# 1. /generate-username
# ---------------------------
ADJECTIVES = [
    "Sunny", "Happy", "Lazy", "Brave", "Funky",
    "Swift", "Golden", "Tiny", "Grand", "Mighty",
    "Cheerful", "Gentle", "Wise", "Lively", "Bold",
    "Calm", "Fierce", "Jolly", "Silly", "Smart"
]

NOUNS = [
    "Fox", "Bear", "Lion", "Cat", "Dog",
    "Eagle", "Shark", "Panda", "Wolf", "Hawk",
    "Tiger", "Rabbit", "Squirrel", "Otter", "Falcon",
    "Dolphin", "Elephant", "Gorilla", "Leopard", "Kangaroo"
]

def generate_username(request):
    first_name = request.GET.get('first_name')
    if first_name:
        # Action 2: Use user's first name with a random number
        random_number = random.randint(100, 999)
        username = f"{first_name}{random_number}"
    else:
        adjective = random.choice(ADJECTIVES)
        noun = random.choice(NOUNS)
        random_code = random.randint(10, 99)
        username = f"{adjective}{noun}{random_code}"

    add_to_history(username)  # Make sure this is defined in your code
    return JsonResponse({'username': username})

# ---------------------------
# 2. /check-username
# ---------------------------
def check_username(request):
    username = request.GET.get('username')
    action = request.GET.get('action')  # '1' or '2'

    if not username:
        return JsonResponse({'error': 'username parameter required'}, status=400)


    is_available = username not in TAKEN_USERNAMES

    if action == '1':

        return JsonResponse({
            'username': username,
            'taken': not is_available
        })
    else:
        return JsonResponse({
            'username': username,
            'available': is_available
        })

# ---------------------------
# 3. /username-suggestions
# ---------------------------
def username_suggestions(request):
    first_name = request.GET.get('first_name')
    favorite_color = request.GET.get('favorite_color')
    suggestions = []

    # Action 1: Suggestions based on first name
    if first_name:
        for _ in range(5):
            random_number = random.randint(10, 99)
            suggestions.append(f"{first_name}{random_number}")
        return JsonResponse({'suggestions': suggestions})

    # Action 2: Suggestions based on favorite color
    elif 'favorite_color' in request.GET:
        if not favorite_color:
            return JsonResponse({'error': 'Please input a color'}, status=400)
        for _ in range(5):
            random_number = random.randint(10, 99)
            suggestions.append(f"{favorite_color}{random_number}")
        return JsonResponse({'suggestions': suggestions})

    else:
        return JsonResponse({'error': 'Please provide either first_name or favorite_color'}, status=400)

# ---------------------------
# 4. /username-length
# ---------------------------
ADJECTIVES = [
    "Sunny", "Happy", "Lazy", "Brave", "Funky",
    "Swift", "Golden", "Tiny", "Grand", "Mighty",
    "Cheerful", "Gentle", "Wise", "Lively", "Bold",
    "Calm", "Fierce", "Jolly", "Silly", "Smart"
]

NOUNS = [
    "Fox", "Bear", "Lion", "Cat", "Dog",
    "Eagle", "Shark", "Panda", "Wolf", "Hawk",
    "Tiger", "Rabbit", "Squirrel", "Otter", "Falcon",
    "Dolphin", "Elephant", "Gorilla", "Leopard", "Kangaroo"
]


def build_humanlike_username_exact_length(req_length):

    if req_length < 3:
        # If length is too short, just return a random string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=req_length))

    # 1) Pick random adjective & noun
    adj = random.choice(ADJECTIVES)
    noun = random.choice(NOUNS)

    # Combine them
    combo = adj + noun
    combo_len = len(combo)

    # 2) Check if combo is already bigger than req_length
    if combo_len > req_length:
        # We'll truncate from the noun first
        space_left = req_length - len(adj)
        if space_left < 0:
            # Even the adjective alone is bigger than req_length, so truncate adjective too
            return adj[:req_length]  # Just return truncated adjective
        else:
            # Truncate the noun to fit
            truncated_noun = noun[:space_left]
            return adj + truncated_noun

    # 3) If there's leftover space, fill with random digits
    leftover = req_length - combo_len
    if leftover > 0:
        digits = ''.join(random.choices(string.digits, k=leftover))
        return combo + digits
    else:
        # combo == req_length exactly
        return combo


@csrf_exempt
def username_length(request):
    """
    4. /username-length

    Action 1 (generate):
      Generate a 'human-like' username with EXACT length 'length'.
      - If 'length' < 3, fallback to a random string of that length.

    Action 2 (check):
      Check if a provided username is within acceptable limits (e.g., 6–20 characters).
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        action = data.get('action')

        if action == 'generate':
            desired_length = data.get('length')
            if not isinstance(desired_length, int):
                return JsonResponse({'error': 'length parameter required and must be an integer'}, status=400)

            # Build a human-like username EXACTLY 'desired_length' long
            username = build_humanlike_username_exact_length(desired_length)

            # Store in history if you want to keep track
            add_to_history(username)
            return JsonResponse({'username': username})

        elif action == 'check':
            username = data.get('username')
            if not username:
                return JsonResponse({'error': 'username parameter required'}, status=400)
            valid = 6 <= len(username) <= 20
            return JsonResponse({'username': username, 'valid_length': valid})

        else:
            return JsonResponse({'error': 'Invalid action. Use "generate" or "check".'}, status=400)

    return JsonResponse({'error': 'POST method required'}, status=400)


# ---------------------------
# 5. /username-complexity
# ---------------------------
@csrf_exempt
def username_complexity(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        action = data.get('action')
        if action == 'generate':
            symbols = "!@#$%^&*"
            all_chars = string.ascii_letters + string.digits + symbols
            username = ''.join(random.choices(all_chars, k=10))
            add_to_history(username)
            return JsonResponse({'username': username})
        elif action == 'check':
            username = data.get('username')
            if not username:
                return JsonResponse({'error': 'username parameter required'}, status=400)
            has_letter = bool(re.search(r'[A-Za-z]', username))
            has_digit = bool(re.search(r'\d', username))
            has_symbol = bool(re.search(r'[!@#$%^&*]', username))
            complexity_ok = has_letter and has_digit and has_symbol
            return JsonResponse({'username': username, 'complexity_ok': complexity_ok})
        else:
            return JsonResponse({'error': 'Invalid action. Use "generate" or "check".'}, status=400)
    return JsonResponse({'error': 'POST method required'}, status=400)

# ---------------------------
# 6. /username-availability
# ---------------------------
def username_availability(request):
    username = request.GET.get('username')
    if not username:
        username = generate_random_username()
    available = username not in TAKEN_USERNAMES
    if not available:
        # Optionally, generate a new username if the provided one is taken
        username = generate_random_username()
        available = username not in TAKEN_USERNAMES
    add_to_history(username)
    return JsonResponse({'username': username, 'available': available})


# ---------------------------
# 7. /username-from-phrase
# ---------------------------
ADJECTIVES = [
    "Sunny", "Happy", "Lazy", "Brave", "Funky",
    "Swift", "Golden", "Tiny", "Grand", "Mighty",
    "Cheerful", "Gentle", "Wise", "Lively", "Bold",
    "Calm", "Fierce", "Jolly", "Silly", "Smart"
]


def username_from_phrase(request):
    phrase = request.GET.get('phrase')
    if not phrase:
        return JsonResponse({'error': 'phrase parameter required'}, status=400)

    # Convert "SummerVacation" -> "Summer_Vacation"
    username_base = re.sub(r'(?<!^)(?=[A-Z])', '_', phrase)

    # Pick a random adjective
    adjective = random.choice(ADJECTIVES)


    current_year = datetime.now().year


    username = f"{adjective}_{username_base}{current_year}"


    unique = request.GET.get('unique', 'false').lower() == 'true'
    if unique:
        username += str(random.randint(10, 99))

    add_to_history(username)

    return JsonResponse({'username': username})

# ---------------------------
# 8. /similar-username-suggestions
# ---------------------------
def similar_username_suggestions(request):
    username = request.GET.get('username')
    if not username:
        return JsonResponse({'error': 'username parameter required'}, status=400)
    suggestions = [
        f"{username}_",
        f"_{username}",
        username.replace("", "_").strip('_'),
        f"{username}{random.randint(10, 99)}",
        f"{username.lower()}"
    ]
    add_to_history(username)
    return JsonResponse({'original': username, 'suggestions': suggestions})

# ---------------------------
# 9. /prefix-username
# ---------------------------
# Uses your custom prefix logic without changes
PREFIX_LIST = [
    "Anti-", "De-", "Dis-", "Em-", "En-", "Fore-", "In-", "Im-", "Inter-",
    "Mid-", "Mis-", "Non-", "Over-", "Pre-", "Re-", "Semi-", "Sub-",
    "Super-", "Trans-", "Un-", "Under-"
]
def prefix_username(request):
    prefix = request.GET.get('prefix')
    if not prefix:
        prefix = random.choice(PREFIX_LIST)
    random_number = random.randint(100, 999)
    username = f"{prefix}{random_number}"
    add_to_history(username)
    return JsonResponse({'username': username})

# ---------------------------
# 10. /suffix-username
# ---------------------------
# Uses your custom suffix logic without changes
ADJECTIVES = [
    "Sunny", "Happy", "Lazy", "Brave", "Funky",
    "Swift", "Golden", "Tiny", "Grand", "Mighty",
    "Cheerful", "Gentle", "Wise", "Lively", "Bold",
    "Calm", "Fierce", "Jolly", "Silly", "Smart"
]

NOUNS = [
    "Fox", "Bear", "Lion", "Cat", "Dog",
    "Eagle", "Shark", "Panda", "Wolf", "Hawk",
    "Tiger", "Rabbit", "Squirrel", "Otter", "Falcon",
    "Dolphin", "Elephant", "Gorilla", "Leopard", "Kangaroo"
]

SUFFIX_LIST = [
    "-er", "-ment", "-ness", "-ion", "-able", "-ous", "-less",
    "-ible", "-like", "-ful", "-ing", "-en", "-ly", "-ward"
]

def suffix_username(request):
    suffix = request.GET.get('suffix')
    if not suffix:

        suffix = random.choice(SUFFIX_LIST)


    adjective = random.choice(ADJECTIVES)
    noun = random.choice(NOUNS)
    base_username = adjective + noun


    username = f"{base_username}{suffix}"


    add_to_history(username)

    return JsonResponse({'username': username})

# ---------------------------
# 11. /username-history
# ---------------------------
@csrf_exempt
def username_history(request):
    if request.method == 'GET':
        return JsonResponse({'history': USERNAME_HISTORY})
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        username_id = data.get('id')
        if username_id is None:
            return JsonResponse({'error': 'id parameter required'}, status=400)
        # First, reset all favorites to False
        for entry in USERNAME_HISTORY:
            entry['favorite'] = False
        # Then mark only the entry with matching id as favorite
        for entry in USERNAME_HISTORY:
            if entry['id'] == username_id:
                entry['favorite'] = True
                return JsonResponse({
                    'message': f"Username {entry['username']} marked as favorite",
                    'entry': entry
                })
        return JsonResponse({'error': 'Username id not found'}, status=404)
    return JsonResponse({'error': 'Unsupported method'}, status=405)

# ---------------------------
# 12. /username-feedback/<int:id>
# ---------------------------
@csrf_exempt
def username_feedback(request, id):
    """
    Action 1: Provide feedback on whether the username is available.
    Action 2: Allow the user to approve or reject the username based on their preferences.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # 1) Optional "feedback" field if you want a textual comment
        feedback = data.get('feedback', '')

        # 2) "preference" field can be "approve" or "reject"
        preference = data.get('preference', '')  # e.g. "approve" or "reject"

        # Find the username history entry by ID
        for entry in USERNAME_HISTORY:
            if entry['id'] == id:
                # Action 1: Check if it's available
                available = entry['username'] not in TAKEN_USERNAMES

                # Action 2: Approve or reject
                # We'll store the preference in the entry for record-keeping
                if preference.lower() in ("approve", "reject"):
                    entry['preference'] = preference.lower()
                else:
                    entry['preference'] = "none"

                # Optionally store textual feedback
                entry['feedback'] = feedback

                # Return updated info
                return JsonResponse({
                    'username': entry['username'],
                    'available': available,
                    'preference': entry['preference'],
                    'feedback': feedback
                })

        return JsonResponse({'error': 'Username id not found'}, status=404)

    return JsonResponse({'error': 'POST method required'}, status=400)
# ---------------------------
# 13. /avoid-special-characters
# ---------------------------
import random, string, re, json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Example adjectives and nouns to form a human-like base
ADJECTIVES = [
    "Sunny", "Happy", "Lazy", "Brave", "Funky",
    "Swift", "Golden", "Tiny", "Grand", "Mighty",
    "Cheerful", "Gentle", "Wise", "Lively", "Bold",
    "Calm", "Fierce", "Jolly", "Silly", "Smart"
]

NOUNS = [
    "Fox", "Bear", "Lion", "Cat", "Dog",
    "Eagle", "Shark", "Panda", "Wolf", "Hawk",
    "Tiger", "Rabbit", "Squirrel", "Otter", "Falcon",
    "Dolphin", "Elephant", "Gorilla", "Leopard", "Kangaroo"
]

@csrf_exempt
def avoid_special_characters(request):
    if request.method == 'GET':

        adjective = random.choice(ADJECTIVES)
        noun = random.choice(NOUNS)
        random_code = str(random.randint(10, 99))
        username = adjective + noun + random_code


        add_to_history(username)

        return JsonResponse({'username': username})

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        username = data.get('username')
        if not username:
            return JsonResponse({'error': 'username parameter required'}, status=400)


        if re.search(r'\W', username):
            alternative = re.sub(r'\W', '', username)
            return JsonResponse({
                'original': username,
                'alternative': alternative,
                'contains_special': True
            })
        return JsonResponse({'username': username, 'contains_special': False})

    return JsonResponse({'error': 'Unsupported method'}, status=405)


# ---------------------------
# 14. /username-variation
# ---------------------------
@csrf_exempt
def username_variation(request):
    if request.method == 'GET':
        # Action 1: Generate variations
        base_username = request.GET.get('username')
        if not base_username:
            return JsonResponse({'error': 'username parameter required'}, status=400)

        # Create sample variations
        variations = [
            base_username + str(random.randint(10, 99)),
            base_username.lower(),
            base_username.upper(),
            base_username[::-1],
            f"{base_username}_{random.randint(1, 9)}"
        ]
        # Filter out taken variations if you want
        available_variations = [v for v in variations if v not in TAKEN_USERNAMES]

        return JsonResponse({
            'base': base_username,
            'variations': available_variations
        })

    elif request.method == 'POST':
        # Action 2: Select a variation and possibly store or reject it
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        selected_variation = data.get('selected')
        if not selected_variation:
            return JsonResponse({'error': 'selected parameter required'}, status=400)

        # Check if it's available
        is_available = selected_variation not in TAKEN_USERNAMES

        # Optional "action" field: "approve" or "reject"
        user_action = data.get('action', '').lower()  # "approve", "reject", or empty
        # Optional feedback
        feedback = data.get('feedback', '')

        # If user "approves" and it is available, store in history
        if user_action == 'approve' and is_available:
            add_to_history(selected_variation)
            # If you want to mark it as "favorite" or store the feedback in the entry, you can do so here.
            # For example, store feedback in the last added entry:
            if feedback:
                USERNAME_HISTORY[-1]['feedback'] = feedback

        # If user "rejects", do nothing (or you could store that info somewhere else)

        return JsonResponse({
            'selected': selected_variation,
            'available': is_available,
            'action': user_action,
            'feedback': feedback
        })

    return JsonResponse({'error': 'Unsupported method'}, status=405)



# ---------------------------
# 15. /filter-inappropriate-words
# ---------------------------
@csrf_exempt
def filter_inappropriate_words(request):
    blacklist = [
        r'arse',
        r'arsehole',
        r'ass',
        r'asshole',
        r'bastard',
        r'bitch',
        r'crap',
        r'cunt',
        r'damn',
        r'dick',
        r'dildo',
        r'fag',
        r'faggot',
        r'fck',
        r'fuck',


        r'\fuck(?:\s*you)?',
        r'\fucker',
        r'\fucking',

        r'holy s*shit',
        r'jesuss*(?:f(?:u)?ck|wept|h\.?\s*christ)',
        r'motherfucker',
        r'prick',
        r'pussy',
        r'shit',
        r'slut',
        r'whore',
        r'twat',
        r'wanker',
        r'wonk',
        r'dickhead',
        r'anakputa',
        r'pakyu',
        r'tite',
    ]

    if request.method == 'GET':
        username = generate_random_username()
        for pattern in blacklist:
            username = re.sub(pattern, '', username, flags=re.IGNORECASE)
        add_to_history(username)
        return JsonResponse({'username': username})
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        username = data.get('username')
        if not username:
            return JsonResponse({'error': 'username parameter required'}, status=400)
        inappropriate = False
        filtered_username = username
        for pattern in blacklist:
            if re.search(pattern, filtered_username, flags=re.IGNORECASE):
                inappropriate = True
                filtered_username = re.sub(pattern, '', filtered_username, flags=re.IGNORECASE)
        if inappropriate:
            return JsonResponse({
                'original': username,
                'alternative': filtered_username,
                'inappropriate': True
            })
        else:
            return JsonResponse({'username': username, 'inappropriate': False})
    return JsonResponse({'error': 'Unsupported method'}, status=405)

# ---------------------------
@csrf_exempt
def custom_username(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # "action" can be "check" or "create"
        action = data.get('action')
        username = data.get('username')

        if not username:
            return JsonResponse({'error': 'username parameter required'}, status=400)

        # Criteria: length 6-20, must include at least one letter and one digit
        valid_length = 6 <= len(username) <= 20
        has_letter = bool(re.search(r'[A-Za-z]', username))
        has_digit = bool(re.search(r'\d', username))
        meets_criteria = valid_length and has_letter and has_digit

        if action == 'check':
            # Action 2: Just confirm if it meets the system's criteria
            return JsonResponse({
                'username': username,
                'meets_criteria': meets_criteria
            })

        elif action == 'create':
            # Action 1: If valid, store in history; otherwise return error
            if meets_criteria:
                add_to_history(username)
                return JsonResponse({
                    'username': username,
                    'created': True
                })
            else:
                return JsonResponse({
                    'username': username,
                    'created': False,
                    'error': 'Username does not meet the required criteria (6-20 chars, letter + digit).'
                })

        else:
            # If "action" is missing or invalid
            return JsonResponse({'error': 'Invalid action. Use "check" or "create".'}, status=400)

    return JsonResponse({'error': 'POST method required'}, status=400)


# ---------------------------
# 17. /random-username-idea
# ---------------------------
@csrf_exempt
def random_username_idea(request):
    if request.method == 'GET':
        username = generate_random_username()
        add_to_history(username)
        return JsonResponse({'username': username})
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        length = data.get('length')
        if not isinstance(length, int):
            return JsonResponse({'error': 'length parameter required and must be an integer'}, status=400)
        username = generate_random_username(length=length)
        add_to_history(username)
        return JsonResponse({'username': username})
    return JsonResponse({'error': 'Unsupported method'}, status=405)

# ---------------------------
# 18. /username-suggestions-by-hobby
# ---------------------------
def username_suggestions_by_hobby(request):
    hobby = request.GET.get('hobby')
    if not hobby:
        return JsonResponse({'error': 'hobby parameter required'}, status=400)
    suggestions = []
    for _ in range(5):
        random_number = random.randint(10, 99)
        suggestions.append(f"{hobby}{random_number}")
    return JsonResponse({'hobby': hobby, 'suggestions': suggestions})

# ---------------------------
# 19. /username-check-similarity
# ---------------------------
def username_check_similarity(request):
    new_username = request.GET.get('new_username')
    existing_username = request.GET.get('existing_username')
    if not new_username or not existing_username:
        return JsonResponse({'error': 'new_username and existing_username parameters required'}, status=400)
    common = set(new_username) & set(existing_username)
    similarity_score = len(common) / max(len(set(new_username)), len(set(existing_username)))
    similar = similarity_score > 0.5
    response = {
        'new_username': new_username,
        'existing_username': existing_username,
        'similar': similar,
        'similarity_score': similarity_score
    }
    if similar:
        response['alternative'] = new_username + "_" + generate_random_username(3)
    return JsonResponse(response)

# ---------------------------
# 20. /username-history-summary
# ---------------------------
@csrf_exempt
def username_history_summary(request):
    if request.method == 'GET':
        summary = {
            'total': len(USERNAME_HISTORY),
            'usernames': [entry['username'] for entry in USERNAME_HISTORY]
        }
        return JsonResponse({'summary': summary})

    elif request.method == 'DELETE':
        # First try the query parameter
        username_id = request.GET.get('id')

        # If not found in query params, check JSON body
        if not username_id:
            try:
                data = json.loads(request.body)
                username_id = data.get('id')
            except json.JSONDecodeError:
                # Instead of "id parameter required", you can say:
                return JsonResponse({'error': 'Please provide an id'}, status=400)

        # If still no username_id after parsing the body
        if not username_id:
            return JsonResponse({'error': 'Please provide an id'}, status=400)

        # Try converting to int
        try:
            username_id = int(username_id)
        except ValueError:
            return JsonResponse({'error': 'id must be an integer'}, status=400)

        # Search for entry
        for entry in USERNAME_HISTORY:
            if entry['id'] == username_id:
                USERNAME_HISTORY.remove(entry)
                return JsonResponse({'message': f"Username {entry['username']} deleted from history."})

        return JsonResponse({'error': 'Username id not found'}, status=404)

    return JsonResponse({'error': 'Unsupported method'}, status=405)


# ---------------------------
# NEW: Single record detail endpoint
# ---------------------------
@csrf_exempt
def username_history_detail(request, id):
    if request.method == 'GET':
        for entry in USERNAME_HISTORY:
            if entry['id'] == id:
                return JsonResponse(entry)
        return JsonResponse({'error': f'Username id {id} not found'}, status=404)
    return JsonResponse({'error': 'GET method required'}, status=405)
