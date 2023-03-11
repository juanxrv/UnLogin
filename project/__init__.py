import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

#Creamos una istancia de SQLAlchemy

db = SQLAlchemy()

#Metodo de inicio de la aplicacion
def create_app():
  #Creamos nuestra aplicacion de Flask
  app = Flask(__name__)

  #Configuraciones necesarias
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['SECRET_KEY'] = os.urandom(24)
  app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:topsecret@localhost:3306/pylogin'

  db.init_app(app)
  # Crear BD en la primera petición
  @app.before_first_request
  def create_all():
    db.create_all()
  
  # Iniciamos el manejo de usuarios
  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)

  #Añadimos la ruta de autenticación
  from .models import User
  @login_manager.user_loader
  def load_user(user_id):
    return User.query.get(int(user_id))

  #Registramos dos blueprints
  from .auth import auth as auth_blueprint
  app.register_blueprint(auth_blueprint)

  from .main import main as main_blueprint
  app.register_blueprint(main_blueprint)

  return app