document.addEventListener('DOMContentLoaded', () => {
    loadContacts();
    setupEventListeners();
});

function setupEventListeners() {
    document.getElementById('addForm').addEventListener('submit', handleAddContact);
    document.getElementById('searchInput').addEventListener('input', handleSearch);
}

async function handleAddContact(e) {
    e.preventDefault();
    const formData = {
        name: document.getElementById('name').value,
        phone: document.getElementById('phone').value,
        email: document.getElementById('email').value
    };

    try {
        const response = await fetch('/contacts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        showMessage('addMessage', result.message, response.ok ? 'success' : 'error');
        if (response.ok) {
            loadContacts();
            document.getElementById('addForm').reset();
        }
    } catch (error) {
        showMessage('addMessage', 'Error adding contact', 'error');
    }
}

function handleSearch(e) {
    const searchTerm = e.target.value.toLowerCase();
    if (searchTerm.length === 0) {
        loadContacts();
        return;
    }
    
    fetch(`/contacts?search=${encodeURIComponent(searchTerm)}`)
        .then(response => response.json())
        .then(contacts => displayContacts(contacts, 'searchResults'))
        .catch(error => console.error('Search error:', error));
}

function loadContacts() {
    fetch('/contacts')
        .then(response => response.json())
        .then(contacts => displayContacts(contacts, 'contactList'))
        .catch(error => console.error('Error loading contacts:', error));
}

function displayContacts(contacts, elementId) {
    const container = document.getElementById(elementId);
    container.innerHTML = contacts.length > 0 
        ? contacts.map(contact => `
            <div>
                <strong>${contact.name}</strong><br>
                Phone: ${contact.phone}<br>
                ${contact.email ? `Email: ${contact.email}` : ''}
            </div>
        `).join('')
        : '<div>No contacts found</div>';
}

function showMessage(elementId, text, type) {
    const messageDiv = document.getElementById(elementId);
    messageDiv.textContent = text;
    messageDiv.className = `message ${type}`;
    setTimeout(() => messageDiv.textContent = '', 3000);
}