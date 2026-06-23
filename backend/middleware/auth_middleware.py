import jwt
import os
from functools import wraps
from flask import request, jsonify


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')

        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'error': 'Token không tồn tại'}), 401

        try:
            payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])
            request.current_user = payload['username']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token đã hết hạn'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token không hợp lệ'}), 401

        return f(*args, **kwargs)
    return decorated
