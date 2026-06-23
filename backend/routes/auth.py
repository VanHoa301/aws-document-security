import jwt
import os
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

# User đơn giản cho demo — thực tế lưu trong DynamoDB
USERS = {
    'admin': 'admin123',
    'user1': 'password1'
}


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not username or not password:
        return jsonify({'error': 'Vui lòng nhập username và password'}), 400

    if USERS.get(username) != password:
        return jsonify({'error': 'Username hoặc password không đúng'}), 401

    token = jwt.encode(
        {
            'username': username,
            'exp': datetime.utcnow() + timedelta(hours=8)
        },
        os.getenv('JWT_SECRET_KEY'),
        algorithm='HS256'
    )

    return jsonify({'token': token, 'username': username})


@auth_bp.route('/verify', methods=['GET'])
def verify():
    from middleware.auth_middleware import require_auth

    @require_auth
    def _verify():
        return jsonify({'username': request.current_user, 'valid': True})

    return _verify()
