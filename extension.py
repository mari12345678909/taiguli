from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import redirect
from flask_login import LoginManager, login_manager

app = Flask(__name__)
app.config["SECRET_KEY"] = "5;eyPylJ94$£"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db: SQLAlchemy = SQLAlchemy(app)

login_manager = LoginManager(app)