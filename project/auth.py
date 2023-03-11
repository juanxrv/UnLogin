from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.get('/login')
def login():
  return render_template('login.html')

@auth.post('/login')
def login_post():
  email = request.form.get('email')
  password = request.form.get('password')
  remember = True if request.form.get('remember') else False

  # Verificamos si existe un usuario con ese correo
  user = User.query.filter_by(email=email).first()
  # Verificamos si la contraseña es correcta
  if not user or not check_password_hash(user.password, password):
    flash('El usuario o contraseña son incorrectos.')
    return redirect(url_for('auth.login'))
  
  # Creamos una sesion
  login_user(user, remember=remember)
  return redirect(url_for('main.profile'))

@auth.get('/signup')
def signup():
  return render_template('signup.html')

@auth.post('/signup')
def signup_post():
  email = request.form.get('email')
  name = request.form.get('name')
  password = request.form.get('password')

  # Verificamos si existe un usuario con ese correo
  user = User.query.filter_by(email=email).first()
  # Verificamos si la contraseña es correcta
  if user:
    flash('El usuario ya existe.')
    return redirect(url_for('auth.signup'))
  
  # Creamos un nuevo usuarioy lo guardamos en la BD
  new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
  db.session.add(new_user)
  db.session.commit()
  return redirect(url_for('auth.login'))

@auth.get('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('main.index'))