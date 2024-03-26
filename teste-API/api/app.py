import json
from flask import Flask, jsonify, request

app = Flask(__name__)

# Carregar dados dos usuários do arquivo JSON
try:
    with open('users_data.json', 'r') as f:
        users = json.load(f)
except FileNotFoundError:
    users = []

# Rota para obter todos os usuários com informações básicas (nome, idade, cpf)
@app.route('/user', methods=['GET'])
def get_users_info():
    print(users)
    users_info = [{'name': u['name'], 'age': u['age'], 'cpf': u['cpf']} for u in users]
    return jsonify(users_info)

@app.route('/user/<int:id_usuario>', methods=['GET'])
def get_user_info(id_usuario):
    users_info = 0
    for u in users:
        if u["id"] == id_usuario:
            users_info = {'name': u['name'], 'age': u['age'], 'cpf': u['cpf']}
            return jsonify(users_info)
    print(id_usuario)
    return 0

# Rota para adicionar um novo usuário
@app.route('/user', methods=['POST'])
def add_user():
    new_user_data = request.json  # Assume que os dados do novo usuário são enviados no corpo da requisição em formato JSON
    if 'name' in new_user_data and 'age' in new_user_data and 'cpf' in new_user_data:
        new_user = {
            'id': len(users) + 1,
            'name': new_user_data['name'],
            'age': new_user_data['age'],
            'cpf': new_user_data['cpf']
        }
        users.append(new_user)
        save_users_to_file(users)
        return jsonify(new_user), 201
    else:
        return jsonify({'message': 'Missing required fields'}), 400

# Função para salvar os dados dos usuários no arquivo JSON
def save_users_to_file(users_data):
    with open('users_data.json', 'w') as f:
        json.dump(users_data, f, indent=4)

if __name__ == '__main__':
    app.run(debug=True)
