import json
from flask import Flask, jsonify, request

app = Flask(__name__)

# Load user data from the JSON file
try:
    with open('data_user.json', 'r') as f:
        users = json.load(f)
except FileNotFoundError:
    users = []

# Route to get all users with basic information (name, age, cpf, email)
@app.route('/user', methods=['GET']) 
def get_users_info():
    users_info = [{'id': u['id'], 'name': u['name'], 'cpf': u['cpf'], 'age': u['age'], 'email': u['email']} for u in users]
    return jsonify(users_info)

# Route to get information of a specific user by ID
@app.route('/user/<int:id_usuario>', methods=['GET'])
def get_user_info(id_usuario):
    for u in users:
        if u["id"] == id_usuario:
            user_info = {'id': u['id'], 'name': u['name'], 'cpf': u['cpf'], 'age': u['age'], 'email': u['email']}
            return jsonify(user_info)
    return jsonify({'message': 'User not found'}), 404

# Route to add a new user
@app.route('/user', methods=['POST'])
def add_user():
    new_user_data = request.json
    if 'name' in new_user_data and 'cpf' in new_user_data and 'age' in new_user_data and 'email' in new_user_data:
        new_user = {
            'id': len(users) + 1,  # Auto-incremented ID
            'name': new_user_data['name'],
            'cpf': new_user_data['cpf'],
            'age': new_user_data['age'],
            'email': new_user_data['email']
        }
        users.append(new_user)
        save_users_to_file(users)
        return jsonify(new_user), 201
    else:
        return jsonify({'message': 'Missing required fields'}), 400

# Function to save user data to the JSON file
def save_users_to_file(users_data):
    with open('data_user.json', 'w') as f:
        json.dump(users_data, f, indent=4)

if __name__ == '__main__':
    app.run(debug=True)
