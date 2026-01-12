# 1. Importe o login_manager do seu __init__.py
from . import db, login_manager 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import DateTime
from datetime import datetime

# 2. Adicione UserMixin na herança da classe
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # Sugestão: Adicione o campo de senha já que você importou as libs de hash
    # password_hash = db.Column(db.String(128)) 
    
    sessions = db.relationship('PomodoroSession', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'
    
    # Métodos opcionais para lidar com senha se você descomentar a linha acima:
    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)
    #
    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)

class PomodoroSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_type = db.Column(db.String(20), nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Session {self.user.email} - {self.session_type} ({self.duration_minutes}m)>'

# 3. A CORREÇÃO PRINCIPAL: A função user_loader
# Sem isso, o Flask-Login não sabe como pegar o usuário do banco pelo ID da sessão
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))