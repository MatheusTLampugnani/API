import json
from flask import Flask, jsonify, request

app = Flask(__name__)

# Load user data from the JSON file
try:
    with open('data_user_validate.json', 'r') as f:
        users = json.load(f)
except FileNotFoundError:
    users = []

# Route to register a new user
@app.route('/register', methods=['POST'])
def register_user():
    new_user_data = request.json
    if 'cpf' in new_user_data and 'password' in new_user_data:
        # Check if the CPF is already registered
        for user in users:
            if user['cpf'] == new_user_data['cpf']:
                return jsonify({'message': 'CPF already registered'}), 400
        
        # Create a new user with auto-incremented ID
        new_user = {
            'id': len(users) + 1,
            'cpf': new_user_data['cpf'],
            'password': new_user_data['password']
        }
        users.append(new_user)
        save_users_to_file(users)
        return jsonify({'message': 'User registered successfully'}), 201
    else:
        return jsonify({'message': 'Missing required fields (cpf, password)'}), 400

# Route for user login
@app.route('/login', methods=['POST'])
def login_user():
    login_data = request.json
    if 'cpf' in login_data and 'password' in login_data:
        for user in users:
            if user['cpf'] == login_data['cpf'] and user['password'] == login_data['password']:
                return jsonify({'message': 'Login successful'}), 200
        return jsonify({'message': 'Invalid credentials'}), 401
    else:
        return jsonify({'message': 'Missing required fields (cpf, password)'}), 400

# Function to save user data to the JSON file
def save_users_to_file(users_data):
    with open('data_user_validate.json', 'w') as f:
        json.dump(users_data, f, indent=4)

if __name__ == '__main__':
    app.run(debug=True)
