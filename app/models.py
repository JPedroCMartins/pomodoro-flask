
from . import db, login_manager 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import DateTime
from datetime import datetime


class User(UserMixin, db.Model):
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



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))