from typing import List, Dict
from datetime import datetime, timedelta
from models import Subject, AcademicTask

def calculate_subject_progress(subject_id: int, db_session) -> Dict:
    """Calcula progresso básico de disciplina: % tarefas concluídas."""
    tasks = db_session.query(AcademicTask).filter_by(subject_id=subject_id).all()
    total_tasks = len(tasks)
    if total_tasks == 0:
        return {'progress_pct': 0, 'total_tasks': 0, 'completed_tasks': 0}
    
    completed = sum(1 for task in tasks if task.status == 'concluida')
    progress_pct = (completed / total_tasks) * 100
    return {
        'progress_pct': round(progress_pct, 2),
        'total_tasks': total_tasks,
        'completed_tasks': completed
    }

def calculate_weighted_progress(user_id: int, db_session) -> Dict:
    """Progresso ponderado por carga_horária (spec requirement)."""
    subjects = db_session.query(Subject).filter_by(user_id=user_id).all()
    
    total_weighted = 0
    total_carga = 0
    subjects_data = []
    
    for subject in subjects:
        prog = calculate_subject_progress(subject.id, db_session)
        weighted = subject.carga_horaria * (prog['progress_pct'] / 100)
        total_weighted += weighted
        total_carga += subject.carga_horaria
        
        subjects_data.append({
            'id': subject.id,
            'name': subject.name,
            'professor': subject.professor,
            'progress_pct': prog['progress_pct'],
            'carga_horaria': subject.carga_horaria,
            'peso': subject.peso,
            'tasks_info': prog
        })
    
    weighted_progress = (total_weighted / total_carga * 100) if total_carga > 0 else 0
    
    return {
        'weighted_progress': round(weighted_progress, 2),
        'total_carga_horaria': total_carga,
        'subjects': subjects_data
    }

def predict_completion_date(user_id: int, db_session) -> Dict:
    """Previsão de conclusão baseada em velocidade atual (insight avançado)."""
    progress_data = calculate_weighted_progress(user_id, db_session)
    if progress_data['weighted_progress'] >= 100:
        return {
            'predicted_date': 'Concluído!',
            'days_remaining': 0,
            'assumption': 'Todas as disciplinas estão 100% concluídas.'
        }
    
    # Simula velocidade: assume 5% progresso/semana (ajustável)
    remaining_progress = 100 - progress_data['weighted_progress']
    weeks_remaining = remaining_progress / 5
    predicted_date = datetime.now() + timedelta(weeks=weeks_remaining)
    
    return {
        'predicted_date': predicted_date.strftime('%d/%m/%Y'),
        'days_remaining': int(weeks_remaining * 7),
        'assumption': '5% progresso/semana médio'
    }
