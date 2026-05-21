from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    professor = db.Column(db.String(100))
    carga_horaria = db.Column(db.Float, default=60.0)  # hours
    peso = db.Column(db.Float, default=1.0)
    description = db.Column(db.Text)
    data_inicio = db.Column(db.Date)
    data_fim = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='subjects')
    academic_tasks = db.relationship(
        'AcademicTask',
        backref='subject',
        lazy=True,
        cascade='all, delete-orphan',
        passive_deletes=True
    )

class AcademicTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    data_prevista = db.Column(db.Date)
    status = db.Column(db.String(20), default='pendente')  # pendente, em_andamento, concluida
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
