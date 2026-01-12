from flask import Blueprint, render_template, request, jsonify, abort
# Removido: from flask_sqlalchemy import SQLAlchemy (não é usado aqui)
from datetime import datetime
# Importação Relativa Corrigida:
from .models import User, PomodoroSession
from . import db

bp = Blueprint('pomo', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/report/<string:email>')
def report(email):
    # Dica: use .first_or_404() para simplificar o código
    user = User.query.filter_by(email=email).first_or_404(description="Usuário não encontrado.")
    
    # Traz as sessões para listar na tabela
    sessions = PomodoroSession.query.filter_by(user_id=user.id).order_by(PomodoroSession.timestamp.desc()).all()
    
    # Otimização: A soma abaixo é feita na memória do Python. 
    # Para produção/escala, seria ideal usar db.session.query(func.sum(...))
    stats = {
        'total_sessions': len(sessions),
        'total_work_min': sum(s.duration_minutes for s in sessions if s.session_type == 'work'),
        'total_short_break_min': sum(s.duration_minutes for s in sessions if s.session_type == 'shortBreak'),
        'total_long_break_min': sum(s.duration_minutes for s in sessions if s.session_type == 'longBreak')
    }
    
    return render_template('report.html', user=user, sessions=sessions, stats=stats)


@bp.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        
        # Validação mais robusta para garantir que data não é None
        if not data or 'email' not in data:
            return jsonify({'success': False, 'error': 'Email é obrigatório'}), 400
            
        email = data.get('email')
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Retornando 200 OK pois a operação foi bem sucedida (o usuário já existe)
            return jsonify({'success': True, 'message': 'Usuário encontrado.'}), 200
        
        new_user = User(email=email)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Usuário registrado com sucesso!'}), 201
    
    except Exception as e:
        db.session.rollback() # Importante rollback em caso de erro no commit
        return jsonify({'success': False, 'error': f'Erro interno: {str(e)}'}), 500

@bp.route('/log_session', methods=['POST'])
def log_session():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Sem dados'}), 400

        email = data.get('email')
        session_type = data.get('type')
        duration = data.get('duration')

        if not all([email, session_type, duration]):
            return jsonify({'success': False, 'error': 'Dados incompletos'}), 400
        
        # Validação de tipo para duração
        try:
            duration_int = int(duration)
        except ValueError:
            return jsonify({'success': False, 'error': 'Duração deve ser um número inteiro'}), 400

        user = User.query.filter_by(email=email).first()
        
        if not user:
            return jsonify({'success': False, 'error': 'Usuário não encontrado.'}), 404
            
        new_session = PomodoroSession(
            session_type=session_type,
            duration_minutes=duration_int,
            user_id=user.id
        )
        db.session.add(new_session)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Sessão registrada!'}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f'Erro ao salvar sessão: {str(e)}'}), 500