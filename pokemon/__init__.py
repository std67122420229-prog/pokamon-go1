import os
from flask import Flask
from pokemon.extensions import db, login_manager, bcrypt
from pokemon.models import User, Type, Pokemon
from pokemon.core.routes import core_bp
from pokemon.users.routes import users_bp
from pokemon.pokemon.routes import pokemon_bp

def create_app():
  app = Flask(__name__)

  # กันพังถ้าไม่มี DATABASE_URL
  app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
  app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'secret123'

  # ✅ ต้อง init ก่อน
  db.init_app(app)
  bcrypt.init_app(app)
  login_manager.init_app(app)

  login_manager.login_view = 'users.login'
  login_manager.login_message = 'Please login before access this page!'
  login_manager.login_message_category = 'warning'

  # ✅ แล้วค่อย create db
  with app.app_context():
    db.create_all()

  app.register_blueprint(core_bp, url_prefix='/')
  app.register_blueprint(users_bp, url_prefix='/users')
  app.register_blueprint(pokemon_bp, url_prefix='/pokemons')

  return app
