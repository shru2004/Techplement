from flask import Flask, render_template, request, jsonify
import json
import re
import os

# FIX 1: Remove duplicate Flask app initialization
app = Flask(__name__, template_folder='templates', static_folder='static')
CONTACTS_FILE = "contacts.json"



# Helper functions (unchanged)
def load_contacts():
    """Load contacts from JSON file"""
    try:
        if not os.path.exists(CONTACTS_FILE) or os.path.getsize(CONTACTS_FILE) == 0:
            return []
            
        with open(CONTACTS_FILE, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading contacts: {e}")
        return []

def save_contacts(contacts):
    """Save contacts to JSON file"""
    try:
        with open(CONTACTS_FILE, 'w') as file:
            json.dump(contacts, file, indent=2)
    except Exception as e:
        print(f"Error saving contacts: {e}")

def validate_phone(phone):
    """Validate phone number (minimum 7 digits)"""
    return phone.isdigit() and len(phone) >= 7

def validate_email(email):
    """Validate email format using regex"""
    if not email:  # Email is optional
        return True
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contacts', methods=['GET'])
def get_contacts():
    search_term = request.args.get('search', '').lower()
    contacts = load_contacts()
    
    if search_term:
        contacts = [c for c in contacts if search_term in c['name'].lower()]
    
    return jsonify(contacts)

@app.route('/contacts', methods=['POST'])
def add_new_contact():
    data = request.get_json()
    contacts = load_contacts()
    
    # Validation checks
    if not data.get('name'):
        return jsonify({'error': 'Name cannot be empty!'}), 400
        
    if any(c['name'].lower() == data['name'].lower() for c in contacts):
        return jsonify({'error': 'Contact already exists!'}), 400
    
    if not validate_phone(data.get('phone', '')):
        return jsonify({'error': 'Invalid phone number! Must be at least 7 digits.'}), 400
    
    if not validate_email(data.get('email', '')):
        return jsonify({'error': 'Invalid email format!'}), 400
    
    contacts.append({
        'name': data['name'],
        'phone': data['phone'],
        'email': data.get('email', '')
    })
    
    save_contacts(contacts)
    return jsonify({'message': 'Contact added successfully!'})

@app.route('/contacts/<name>', methods=['PUT'])
def update_existing_contact(name):
    contacts = load_contacts()
    data = request.get_json()
    
    # Find the contact to update
    contact_index = next((i for i, c in enumerate(contacts) if c['name'].lower() == name.lower()), None)

    
    if contact_index is None:
        return jsonify({'error': 'Contact not found!'}), 404

    # Validate updates
    updated_data = {}
    if 'name' in data:
        # FIX 2: Prevent false positive on name update check
        new_name = data['name'].lower()
        if any(i != contact_index and c['name'].lower() == new_name for i, c in enumerate(contacts)):
            return jsonify({'error': 'New name already exists!'}), 400
        updated_data['name'] = data['name']
    
    if 'phone' in data:
        if not validate_phone(data['phone']):
            return jsonify({'error': 'Invalid phone number!'}), 400
        updated_data['phone'] = data['phone']
    
    if 'email' in data:
        if not validate_email(data['email']):
            return jsonify({'error': 'Invalid email format!'}), 400
        updated_data['email'] = data['email']

    # Apply updates
    contacts[contact_index].update(updated_data)
    save_contacts(contacts)
    return jsonify({'message': 'Contact updated successfully!'})


if __name__ == '__main__':
    app.run(debug=True)

    