from flask import Flask, render_template, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

base_dir = os.path.abspath(os.path.dirname(__file__))

data_dir = os.path.join(base_dir, 'data')
os.makedirs(data_dir, exist_ok=True) 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(data_dir, 'pomodoro.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    sessions = db.relationship('PomodoroSession', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'

class PomodoroSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_type = db.Column(db.String(20), nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Session {self.user.email} - {self.session_type} ({self.duration_minutes}m)>'

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/report/<string:email>')
def report(email):
    user = User.query.filter_by(email=email).first()
    
    if not user:
        abort(404, description="Usuário não encontrado.")
        
    sessions = PomodoroSession.query.filter_by(user_id=user.id).order_by(PomodoroSession.timestamp.desc()).all()
    
    stats = {
        'total_sessions': len(sessions),
        'total_work_min': sum(s.duration_minutes for s in sessions if s.session_type == 'work'),
        'total_short_break_min': sum(s.duration_minutes for s in sessions if s.session_type == 'shortBreak'),
        'total_long_break_min': sum(s.duration_minutes for s in sessions if s.session_type == 'longBreak')
    }
    
    return render_template('report.html', user=user, sessions=sessions, stats=stats)


@app.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'Requisição sem JSON ou corpo vazio.'}), 400
            
        email = data.get('email')

        if not email:
            return jsonify({'success': False, 'error': 'Email é obrigatório'}), 400
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            return jsonify({'success': True, 'message': 'Usuário encontrado.'})
        
        new_user = User(email=email)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Usuário registrado com sucesso!'}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f'Erro interno do servidor: {str(e)}'}), 500

@app.route('/log_session', methods=['POST'])
def log_session():
    try:
        data = request.get_json()
        email = data.get('email')
        session_type = data.get('type')
        duration = data.get('duration')

        if not all([email, session_type, duration]):
            return jsonify({'success': False, 'error': 'Dados incompletos'}), 400
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return jsonify({'success': False, 'error': 'Usuário não encontrado. Registre-se primeiro.'}), 404
            
        new_session = PomodoroSession(
            session_type=session_type,
            duration_minutes=int(duration),
            user_id=user.id
        )
        db.session.add(new_session)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Sessão registrada!'}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f'Erro ao salvar sessão: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)