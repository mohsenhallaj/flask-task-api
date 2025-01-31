from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app import mongo
from app.utils import hash_password, check_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    if mongo.db.users.find_one({'username': username}):
        return jsonify({'error': 'User already exists'}), 400

    hashed_password = hash_password(password)
    mongo.db.users.insert_one({'username': username, 'password': hashed_password, 'role': role})

    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = mongo.db.users.find_one({'username': username})
    if not user or not check_password(password, user['password']):
        return jsonify({'msg': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=username, additional_claims={"role": user.get("role", "user")})
    return jsonify(access_token=access_token)
