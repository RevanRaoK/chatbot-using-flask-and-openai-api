from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path, makedirs
# write the code for creating and object of SQLAlchemy
db = SQLAlchemy()
DB_NAME = "database.db"
# Base directory for the websote package
BASEDIR = path.abspath(path.dirname(__file__))


def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = "Simple Secret Key"
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  # Write the code for adding your database to the application here
  DB_PATH = path.join(BASEDIR, DB_NAME)
  app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
  # Initialize the db with this app
  db.init_app(app)
  # call your database here
  # Ensure database + tables exists
  create_database(app)
  # Register blueprints
  from .routes import routes
  app.register_blueprint(routes, url_prefix="/")
  return app
# Write the code for your database method here


def create_database(app):
  """Create the SQLite databased + tables if they don't exist."""
  with app.app_context():
    from .models import Result
    db.create_all()
    print("Database Initialized and Tables Created")
