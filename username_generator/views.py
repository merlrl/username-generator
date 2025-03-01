from django.http import JsonResponse
import random, string, json, re
from datetime import datetime

# Add this import for disabling CSRF checks on certain views
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
    NEXT_ID += 1
    return entry

def generate_random_username(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# ---------------------------
# 1. /generate-username
# (GET only; no POST -> no @csrf_exempt needed)
# ---------------------------
def generate_username(request):
    first_name = request.GET.get('first_name')
    if first_name:
        random_number = random.randint(100, 999)
        username = f"{first_name}{random_number}"
    else:
        username = generate_random_username()
    add_to_history(username)
    return JsonResponse({'username': username})

# ---------------------------
# 2. /check-username
# (GET only; no POST -> no @csrf_exempt needed)
# ---------------------------
def check_username(request):
    username = request.GET.get('username')
    if not username:
        return JsonResponse({'error': 'username parameter required'}, status=400)
    available = username not in TAKEN_USERNAMES
    return JsonResponse({'username': username, 'available': available})

# ---------------------------
# 3. /username-suggestions
# (GET only; no POST -> no @csrf_exempt needed)
# ---------------------------
def username_suggestions(request):
    first_name = request.GET.get('first_name')
    favorite_color = request.GET.get('favorite_color')
    suggestions = []
    if first_name:
        for _ in range(5):
            random_number = random.randint(10, 99)
            suggestions.append(f"{first_name}{random_number}")
    elif favorite_color:
        for _ in range(5):
            random_number = random.randint(10, 99)
            suggestions.append(f"{favorite_color}{random_number}")
    else:
        return JsonResponse({'error': 'first_name or favorite_color parameter required'}, status=400)
    return JsonResponse({'suggestions': suggestions})

# ---------------------------
# 4. /username-length
# (Handles POST -> add @csrf_exempt)
# ---------------------------
@csrf_exempt
def username_length(request):
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
            username = generate_random_username(length=desired_length)
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
# (Handles POST -> add @csrf_exempt)
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
# (GET only; no POST -> no @csrf_exempt needed)
# ---------------------------
def username_availability(request):
    username = request.GET.get('username')
    if not username:
        username = generate_random_username()
    available = username not in TAKEN_USERNAMES
    if not available:
        username = generate_random_username()
        available = username not in TAKEN_USERNAMES
    add_to_history(username)
    return JsonResponse({'username': username, 'available': available})

# ---------------------------
# 7. /username-from-phrase
# (GET only; no POST -> no @csrf_exempt needed)
# ---------------------------
def username_from_phrase(request):
    phrase = request.GET.get('phrase')
    if not phrase:
        return JsonResponse({'error': 'phrase parameter required'}, status=400)
    current_year = datetime.now().year
    username_base = re.sub(r'(?<!^)(?=[A-Z])', '_', phrase)
    username = f"{username_base}{current_year}"
    unique = request.GET.get('unique', 'false').lower() == 'true'
    if unique:
        username += str(random.randint(10, 99))
    add_to_history(username)
    return JsonResponse({'username': username})

# ---------------------------
# 8. /similar-username-suggestions
# (GET only; no POST -> no @csrf_exempt needed)
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
    return JsonResponse({'original': username, 'suggestions': suggestions})

# ---------------------------
# 9. /prefix-username
# (GET only; no POST -> no @csrf_exempt needed)
# ---------------------------
def prefix_username(request):
    prefix = request.GET.get('prefix')
    if not prefix:
        prefix = "CoolUser"
    username = f"{prefix}{random.randint(100, 999)}"
    add_to_history(username)
    return JsonResponse({'username': username})

# ---------------------------
# 10. /suffix-username
# (GET only; no POST -> no @csrf_exempt needed)
# ---------------------------
def suffix_username(request):
    suffix = request.GET.get('suffix')
    if not suffix:
        suffix = "User2023"
    username = f"{generate_random_username(5)}{suffix}"
    add_to_history(username)
    return JsonResponse({'username': username})

# ---------------------------
# 11. /username-history
# (Handles GET and POST -> add @csrf_exempt)
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
        for entry in USERNAME_HISTORY:
            if entry['id'] == username_id:
                entry['favorite'] = True
                return JsonResponse({'message': f"Username {entry['username']} marked as favorite", 'entry': entry})
        return JsonResponse({'error': 'Username id not found'}, status=404)
    return JsonResponse({'error': 'Unsupported method'}, status=405)

# ---------------------------
# 12. /username-feedback/<int:id>
# (Handles POST -> add @csrf_exempt)
# ---------------------------
@csrf_exempt
def username_feedback(request, id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        feedback = data.get('feedback')
        for entry in USERNAME_HISTORY:
            if entry['id'] == id:
                available = entry['username'] not in TAKEN_USERNAMES
                entry['feedback'] = feedback
                return JsonResponse({
                    'username': entry['username'],
                    'available': available,
                    'feedback': feedback
                })
        return JsonResponse({'error': 'Username id not found'}, status=404)
    return JsonResponse({'error': 'POST method required'}, status=400)

# ---------------------------
# 13. /avoid-special-characters
# (Handles GET and POST -> add @csrf_exempt)
# ---------------------------
@csrf_exempt
def avoid_special_characters(request):
    if request.method == 'GET':
        username = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
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
# (GET only; no POST -> no @csrf_exempt needed)
# ---------------------------
def username_variation(request):
    base_username = request.GET.get('username')
    if not base_username:
        return JsonResponse({'error': 'username parameter required'}, status=400)
    variations = [
        base_username + str(random.randint(10, 99)),
        base_username.lower(),
        base_username.upper(),
        base_username[::-1],
        f"{base_username}_{random.randint(1, 9)}"
    ]
    available_variations = [u for u in variations if u not in TAKEN_USERNAMES]
    return JsonResponse({'base': base_username, 'variations': available_variations})

# ---------------------------
# 15. /filter-inappropriate-words
# (Handles GET and POST -> add @csrf_exempt)
# ---------------------------
@csrf_exempt
def filter_inappropriate_words(request):
    blacklist = {"badword", "inappropriate"}
    if request.method == 'GET':
        username = generate_random_username()
        for word in blacklist:
            username = username.replace(word, '')
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
        found_bad = [word for word in blacklist if word in username.lower()]
        if found_bad:
            alternative = username
            for word in found_bad:
                alternative = alternative.replace(word, '')
            return JsonResponse({
                'original': username,
                'alternative': alternative,
                'inappropriate': True
            })
        return JsonResponse({'username': username, 'inappropriate': False})
    return JsonResponse({'error': 'Unsupported method'}, status=405)

# ---------------------------
# 16. /custom-username
# (Handles POST -> add @csrf_exempt)
# ---------------------------
@csrf_exempt
def custom_username(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        username = data.get('username')
        if not username:
            return JsonResponse({'error': 'username parameter required'}, status=400)
        # Validate: length between 6-20, at least one letter and one digit
        valid_length = 6 <= len(username) <= 20
        has_letter = bool(re.search(r'[A-Za-z]', username))
        has_digit = bool(re.search(r'\d', username))
        if valid_length and has_letter and has_digit:
            add_to_history(username)
            return JsonResponse({'username': username, 'valid': True})
        return JsonResponse({
            'username': username,
            'valid': False,
            'error': 'Username does not meet criteria (6-20 characters, includes at least one letter and one digit)'
        })
    return JsonResponse({'error': 'POST method required'}, status=400)

# ---------------------------
# 17. /random-username-idea
# (Handles GET and POST -> add @csrf_exempt)
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
# (GET only; no POST -> no @csrf_exempt needed)
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
# (GET only; no POST -> no @csrf_exempt needed)
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
# (Handles GET and DELETE -> add @csrf_exempt for DELETE)
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
        username_id = request.GET.get('id')
        if not username_id:
            try:
                data = json.loads(request.body)
                username_id = data.get('id')
            except json.JSONDecodeError:
                return JsonResponse({'error': 'id parameter required'}, status=400)
        try:
            username_id = int(username_id)
        except ValueError:
            return JsonResponse({'error': 'id must be an integer'}, status=400)
        for entry in USERNAME_HISTORY:
            if entry['id'] == username_id:
                USERNAME_HISTORY.remove(entry)
                return JsonResponse({'message': f"Username {entry['username']} deleted from history."})
        return JsonResponse({'error': 'Username id not found'}, status=404)
    return JsonResponse({'error': 'Unsupported method'}, status=405)
