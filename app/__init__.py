from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123ghost@localhost/app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hard to guess'
UPLOAD_FOLDER = 'img'
UPLOAD_FILE = 'file'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FILE'] = UPLOAD_FILE
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'sign_in'

from app import routes, model