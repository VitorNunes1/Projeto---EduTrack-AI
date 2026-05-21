from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import jsonify, request
from models import db, User
from datetime import timedelta

def register_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email já cadastrado'}), 400
    
    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'Usuário criado com sucesso'}), 201

def login_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(
            identity=str(user.id),
            expires_delta=timedelta(hours=24)
        )
        return jsonify({'access_token': access_token, 'user_id': user.id})
    
    return jsonify({'error': 'Credenciais inválidas'}), 401

def get_current_user():
    user_id = get_jwt_identity()
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return None
    user = User.query.get(user_id)
    return user
