from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# 1. Defina as extensões globalmente aqui, mas não as vincule ao app ainda.
# Isso permite que 'models.py' e 'routes.py' importem 'db' sem erro de importação circular.
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Configurações de Caminho
    base_dir = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True) 

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(data_dir, 'pomodoro.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 2. Inicialize as extensões com o app criado
    db.init_app(app)
    
    login_manager.login_view = 'login' # Nome da função da view de login
    login_manager.init_app(app)
    
    # 3. Importe e registre as rotas/blueprints APÓS a inicialização do app
    # Isso evita importações circulares se 'routes' precisar importar 'app' ou 'db'
    from . import routes
    app.register_blueprint(routes.bp)
    
    # Criação do banco de dados
    with app.app_context():
        db.create_all()

    return app