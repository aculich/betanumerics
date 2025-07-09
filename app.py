import os
import hashlib
import random
import string
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# In-memory storage for user sessions and last identifiers
# In production, this should be replaced with a proper database
user_sessions = {}
last_identifiers = {}

# Betanumeric character set (excluding vowels and 'l')
BETANUMERIC_CHARS = 'bcdfghjkmnpqrstvwxz0123456789'

def hash_email(email):
    """Create an opaque hash of the email address"""
    return hashlib.sha256(email.encode()).hexdigest()[:16]

def generate_check_digit(identifier):
    """Generate a simple check digit for error detection"""
    # Simple checksum: sum of character positions mod 36
    total = sum(ord(c) for c in identifier)
    check_char = BETANUMERIC_CHARS[total % len(BETANUMERIC_CHARS)]
    return check_char

def generate_betanumeric(length=3):
    """Generate a betanumeric identifier of specified length"""
    # Ensure no more than 2 letters in a row
    result = []
    letter_count = 0
    
    for i in range(length - 1):  # Leave room for check digit
        if letter_count >= 2:
            # Force a digit
            char = random.choice('0123456789')
            letter_count = 0
        else:
            char = random.choice(BETANUMERIC_CHARS)
            if char.isalpha():
                letter_count += 1
            else:
                letter_count = 0
        result.append(char)
    
    identifier = ''.join(result)
    check_digit = generate_check_digit(identifier)
    return identifier + check_digit

def get_next_identifier(email, last_identifier=None):
    """Get the next unique identifier for a user"""
    if email not in last_identifiers:
        # First identifier for this user
        identifier = generate_betanumeric(3)
        last_identifiers[email] = identifier
        return identifier
    
    # For now, just generate a new random identifier
    # In a real implementation, you'd want to track and increment properly
    identifier = generate_betanumeric(3)
    last_identifiers[email] = identifier
    return identifier

def is_slug_easter_egg(email):
    """Check if the email triggers the slug/lug easter egg"""
    email_lower = email.lower().strip()
    return email_lower in ['slug', 'lug']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_identifier():
    data = request.get_json()
    email = data.get('email', '').strip()
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    # Check for slug/lug easter egg
    if is_slug_easter_egg(email):
        return jsonify({
            'identifier': 'SLG',
            'url': f"https://betanumerics.app/u/{hash_email(email)}/id/SLG",
            'easter_egg': True,
            'message': 'You found the secret slug/lug!'
        })
    
    # Generate identifier
    last_identifier = data.get('last_identifier')
    identifier = get_next_identifier(email, last_identifier)
    
    # Create opaque user ID
    opaque_user_id = hash_email(email)
    
    # Generate URL
    url = f"https://betanumerics.app/u/{opaque_user_id}/id/{identifier}"
    
    # Store in user session
    if email not in user_sessions:
        user_sessions[email] = []
    user_sessions[email].append({
        'identifier': identifier,
        'url': url,
        'timestamp': 'now'  # In production, use actual timestamp
    })
    
    return jsonify({
        'identifier': identifier,
        'url': url,
        'easter_egg': False
    })

@app.route('/u/<opaque_user_id>/id/<identifier>')
def view_identifier(opaque_user_id, identifier):
    # In a real implementation, you'd validate the opaque_user_id
    # and check if the identifier exists for that user
    return render_template('view_identifier.html', 
                         identifier=identifier, 
                         opaque_user_id=opaque_user_id)

@app.route('/api/generate', methods=['POST'])
def api_generate():
    """API endpoint for programmatic access"""
    data = request.get_json()
    email = data.get('email', '').strip()
    last_identifier = data.get('last_identifier')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    # Check for slug/lug easter egg
    if is_slug_easter_egg(email):
        return jsonify({
            'identifier': 'SLG',
            'url': f"https://betanumerics.app/u/{hash_email(email)}/id/SLG",
            'easter_egg': True,
            'message': 'You found the secret slug/lug!'
        })
    
    # Generate identifier
    identifier = get_next_identifier(email, last_identifier)
    opaque_user_id = hash_email(email)
    url = f"https://betanumerics.app/u/{opaque_user_id}/id/{identifier}"
    
    return jsonify({
        'identifier': identifier,
        'url': url,
        'easter_egg': False
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True) 