import json
import re
import os

CONTACTS_FILE = "contacts.json"

def load_contacts():
    """Load contacts from JSON file"""
    try:
        with open(CONTACTS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
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

def add_contact(contacts):
    """Add a new contact with validation"""
    name = input("Enter name: ").strip()
    if not name:
        print("Error: Name cannot be empty!")
        return
    
    # Check for existing contact
    if any(c['name'].lower() == name.lower() for c in contacts):
        print("Error: Contact already exists!")
        return
    
    phone = input("Enter phone number: ").strip()
    if not validate_phone(phone):
        print("Error: Invalid phone number (must be at least 7 digits)")
        return
    
    email = input("Enter email (optional): ").strip()
    if not validate_email(email):
        print("Error: Invalid email format!")
        return
    
    contacts.append({'name': name, 'phone': phone, 'email': email})
    save_contacts(contacts)
    print("Contact added successfully!")

def search_contacts(contacts):
    """Search contacts by name (case-insensitive partial match)"""
    search_term = input("Enter name to search: ").strip().lower()
    results = [c for c in contacts if search_term in c['name'].lower()]
    
    if not results:
        print("No contacts found")
        return
    
    print(f"\nFound {len(results)} contact(s):")
    for idx, contact in enumerate(results, 1):
        print(f"{idx}. {contact['name']} - {contact['phone']} - {contact['email']}")

def update_contact(contacts):
    """Update existing contact information"""
    search_term = input("Enter name of contact to update: ").strip().lower()
    matches = [c for c in contacts if search_term in c['name'].lower()]
    
    if not matches:
        print("Contact not found")
        return
    
    print("\nMatching contacts:")
    for idx, contact in enumerate(matches, 1):
        print(f"{idx}. {contact['name']}")
    
    try:
        selection = int(input("\nEnter number to update: "))
        if not (1 <= selection <= len(matches)):
            raise ValueError
    except ValueError:
        print("Error: Invalid selection")
        return
    
    contact = matches[selection-1]
    
    print("\nEnter new values (press Enter to keep current)")
    new_name = input(f"Name ({contact['name']}): ").strip()
    new_phone = input(f"Phone ({contact['phone']}): ").strip()
    new_email = input(f"Email ({contact['email']}): ").strip()
    
    # Validate and update name
    if new_name:
        if any(c['name'].lower() == new_name.lower() for c in contacts):
            print("Error: Name already exists in contacts!")
            return
        contact['name'] = new_name
    
    # Validate and update phone
    if new_phone:
        if not validate_phone(new_phone):
            print("Error: Invalid phone number")
            return
        contact['phone'] = new_phone
    
    # Validate and update email
    if new_email:
        if not validate_email(new_email):
            print("Error: Invalid email format")
            return
        contact['email'] = new_email
    
    save_contacts(contacts)
    print("Contact updated successfully!")

def list_contacts(contacts):
    """Display all contacts in the database"""
    if not contacts:
        print("No contacts found in database.")
        return
    
    print("\nAll Contacts:")
    for idx, contact in enumerate(contacts, 1):
        print(f"{idx}. {contact['name']}")
        print(f"   Phone: {contact['phone']}")
        print(f"   Email: {contact['email']}\n")

def main_menu():
    """Main command-line interface"""
    contacts = load_contacts()
    
    while True:
        print("\nContact Management System")
        print("1. Add Contact")
        print("2. Search Contacts")
        print("3. Update Contact")
        print("4. List All Contacts")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            add_contact(contacts)
        elif choice == '2':
            search_contacts(contacts)
        elif choice == '3':
            update_contact(contacts)
        elif choice == '4':
            list_contacts(contacts)
        elif choice == '5':
            save_contacts(contacts)
            print("Goodbye!")
            break
        else:
            print("Error: Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main_menu()