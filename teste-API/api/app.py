import json
from flask import Flask, jsonify, request

app = Flask(__name__)

# Load user data from 'user_data.json'
try:
    with open('user_data.json', 'r') as f:
        users = json.load(f)
except FileNotFoundError:
    users = []

# Load login data from 'user_log.json'
try:
    with open('user_log.json', 'r') as f:
        logins = json.load(f)
except FileNotFoundError:
    logins = []

# Route to get all users with basic information (id, name, cpf, email, age)
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/users/<int:id_usuario>', methods=['GET'])
def get_user_info(id_usuario):
    for u in users:
        if u["id"] == id_usuario:
            user_info = {'id': u['id'], 'name': u['name'], 'cpf': u['cpf'], 'email': u['email'], 'age': u['age']}
            return jsonify(user_info)
    return jsonify({'message': 'User not found'}), 404

# Route to add a new user
@app.route('/user', methods=['POST'])
def add_user():
    new_user_data = request.json
    if 'name' in new_user_data and 'cpf' in new_user_data and 'email' in new_user_data and 'age' in new_user_data:
        new_user = {
            'id': len(users) + 1,
            'name': new_user_data['name'],
            'cpf': new_user_data['cpf'],
            'email': new_user_data['email'],
            'age': new_user_data['age']
        }
        users.append(new_user)
        save_users_to_file(users)
        return jsonify({'message': 'User added successfully'}), 201
    else:
        return jsonify({'message': 'Missing required fields (id, name, cpf, email, age)'}), 400

# Route to delete a user by ID
@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    global users
    users = [u for u in users if u['id'] != id]
    save_users_to_file(users)
    return jsonify({'message': 'User deleted successfully'}), 200

# Route for user login or registration
@app.route('/login', methods=['POST'])
def login_or_register():
    login_data = request.json
    if 'cpf' in login_data and 'password' in login_data:
        for login in logins:
            if login['cpf'] == login_data['cpf'] and login['password'] == login_data['password']:
                return jsonify({'message': 'Login successful'}), 200
        return jsonify({'message': 'Invalid credentials'}), 401
    else:
        return jsonify({'message': 'Missing required fields (cpf, password)'}), 400

# Route to register a new login
@app.route('/register', methods=['POST'])
def register_login():
    new_login_data = request.json
    if 'cpf' in new_login_data and 'password' in new_login_data:
        # Check if the CPF is already registered
        for login in logins:
            if login['cpf'] == new_login_data['cpf']:
                return jsonify({'message': 'CPF already registered'}), 400
        
        # Create a new login
        new_login = {
            'cpf': new_login_data['cpf'],
            'password': new_login_data['password']
        }
        logins.append(new_login)
        save_logins_to_file(logins)
        return jsonify({'message': 'Login registered successfully'}), 201
    else:
        return jsonify({'message': 'Missing required fields (cpf, password)'}), 400

# Function to save user data to 'user_data.json'
def save_users_to_file(users_data):
    with open('user_data.json', 'w') as f:
        json.dump(users_data, f, indent=4)

# Function to save login data to 'user_log.json'
def save_logins_to_file(logins_data):
    with open('user_log.json', 'w') as f:
        json.dump(logins_data, f, indent=4)

if __name__ == '__main__':
    app.run(debug=True)
