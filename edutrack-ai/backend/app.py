from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from models import db, User, Subject, AcademicTask
from auth import register_user, login_user, get_current_user
from progress_calculator import calculate_subject_progress, calculate_weighted_progress, predict_completion_date
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'edutrack-super-secret-key-2026'  # Change in prod
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # Long-lived for demo

db.init_app(app)
jwt = JWTManager(app)
CORS(app)

with app.app_context():
    db.create_all()

# AUTH
@app.route('/api/auth/register', methods=['POST'])
def api_register():
    return register_user()

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    return login_user()

# SUBJECTS (Disciplinas)
@app.route('/api/subjects', methods=['GET', 'POST'])
@jwt_required()
def handle_subjects():
    user_id = int(get_jwt_identity())

    if request.method == 'POST':
        data = request.get_json() or {}
        if not data.get('name'):
            return jsonify({'error': 'Nome da disciplina é obrigatório'}), 400

        subject = Subject(
            user_id=user_id,
            name=data['name'],
            professor=data.get('professor', ''),
            carga_horaria=float(data.get('carga_horaria', 60.0)),
            peso=float(data.get('peso', 1.0)),
            description=data.get('description', ''),
            data_inicio=datetime.strptime(data['data_inicio'], '%Y-%m-%d').date() if data.get('data_inicio') else None,
            data_fim=datetime.strptime(data['data_fim'], '%Y-%m-%d').date() if data.get('data_fim') else None
        )
        db.session.add(subject)
        db.session.commit()
        return jsonify({'message': 'Disciplina criada', 'id': subject.id}), 201

    subjects = Subject.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': s.id, 'name': s.name, 'professor': s.professor,
        'carga_horaria': s.carga_horaria, 'peso': s.peso, 'description': s.description,
        'data_inicio': s.data_inicio.isoformat() if s.data_inicio else None,
        'data_fim': s.data_fim.isoformat() if s.data_fim else None
    } for s in subjects])

@app.route('/api/subjects/<int:subject_id>', methods=['PUT', 'DELETE'])
@jwt_required()
def handle_subject(subject_id):
    user_id = int(get_jwt_identity())
    subject = Subject.query.filter_by(id=subject_id, user_id=user_id).first()
    if not subject:
        return jsonify({'error': 'Disciplina não encontrada'}), 404

    if request.method == 'DELETE':
        db.session.delete(subject)
        db.session.commit()
        return jsonify({'message': 'Disciplina excluída'})

    data = request.get_json() or {}
    subject.name = data.get('name', subject.name)
    subject.professor = data.get('professor', subject.professor)
    subject.carga_horaria = float(data.get('carga_horaria', subject.carga_horaria))
    subject.peso = float(data.get('peso', subject.peso))
    subject.description = data.get('description', subject.description)
    subject.data_inicio = datetime.strptime(data['data_inicio'], '%Y-%m-%d').date() if data.get('data_inicio') else subject.data_inicio
    subject.data_fim = datetime.strptime(data['data_fim'], '%Y-%m-%d').date() if data.get('data_fim') else subject.data_fim
    db.session.commit()
    return jsonify({'message': 'Disciplina atualizada'})

# TASKS (Tarefas Acadêmicas)
@app.route('/api/tasks/<int:subject_id>', methods=['GET', 'POST'])
@jwt_required()
def handle_tasks(subject_id):
    user_id = int(get_jwt_identity())
    subject = Subject.query.filter_by(id=subject_id, user_id=user_id).first()
    if not subject:
        return jsonify({'error': 'Disciplina não encontrada'}), 404
    
    if request.method == 'POST':
        data = request.get_json() or {}
        if not data.get('title'):
            return jsonify({'error': 'Título da tarefa é obrigatório'}), 400

        task = AcademicTask(
            subject_id=subject_id,
            title=data['title'],
            description=data.get('description', ''),
            data_prevista=datetime.strptime(data['data_prevista'], '%Y-%m-%d').date() if data.get('data_prevista') else None,
            status=data.get('status', 'pendente')
        )
        db.session.add(task)
        db.session.commit()
        return jsonify({'message': 'Tarefa criada', 'id': task.id}), 201
    
    # GET
    tasks = AcademicTask.query.filter_by(subject_id=subject_id).all()
    return jsonify([{
        'id': t.id, 'title': t.title, 'description': t.description,
        'data_prevista': t.data_prevista.isoformat() if t.data_prevista else None,
        'status': t.status
    } for t in tasks])

@app.route('/api/tasks/<int:task_id>', methods=['PUT', 'DELETE'])
@jwt_required()
def update_task(task_id):
    user_id = int(get_jwt_identity())
    task = AcademicTask.query.join(Subject).filter(
        AcademicTask.id == task_id,
        Subject.user_id == user_id
    ).first()
    if not task:
        return jsonify({'error': 'Tarefa não encontrada'}), 404

    if request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Tarefa excluída'})

    data = request.get_json() or {}
    task.status = data.get('status', task.status)
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)

    if data.get('data_prevista'):
        task.data_prevista = datetime.strptime(data['data_prevista'], '%Y-%m-%d').date()

    db.session.commit()
    return jsonify({'message': 'Tarefa atualizada'})

# DASHBOARD
@app.route('/api/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    user_id = int(get_jwt_identity())
    weighted = calculate_weighted_progress(user_id, db.session)
    prediction = predict_completion_date(user_id, db.session)
    return jsonify({
        'weighted_progress': weighted['weighted_progress'],
        'total_carga_horaria': weighted['total_carga_horaria'],
        'subjects': weighted['subjects'],
        'prediction': prediction
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
