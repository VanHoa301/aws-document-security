import os
from datetime import datetime, timedelta

import jwt
from flask import Blueprint, jsonify, request

auth_bp = Blueprint('auth', __name__)

# Demo users. In production, use DynamoDB/Cognito or another identity provider.
USERS = {
    'admin': {'password': 'admin123', 'role': 'admin'},
    'user1': {'password': 'password1', 'role': 'user'},
}


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user = USERS.get(username)
    if not user or user['password'] != password:
        return jsonify({'error': 'Username or password is incorrect'}), 401

    secret = os.getenv('JWT_SECRET_KEY')
    if not secret:
        return jsonify({'error': 'JWT_SECRET_KEY is not configured'}), 500

    token = jwt.encode(
        {
            'username': username,
            'role': user['role'],
            'exp': datetime.utcnow() + timedelta(hours=8),
        },
        secret,
        algorithm='HS256',
    )

    return jsonify({'token': token, 'username': username, 'role': user['role']})


@auth_bp.route('/verify', methods=['GET'])
def verify():
    from middleware.auth_middleware import require_auth

    @require_auth
    def _verify():
        return jsonify({
            'username': request.current_user,
            'role': request.current_role,
            'valid': True,
        })

    return _verify()
