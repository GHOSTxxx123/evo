from app import app, db
from sqlalchemy.sql import func
from dataclasses import dataclass
from datetime import datetime
from flask_login import UserMixin


@dataclass
class Compani(db.Model):
    id: int
    Campaning_Name: str
    Collection_Pointer: int
    Buffer_Pointer: int
    Status: str
    Attempts: int
    License_In_Use : int
    First_Call_Time: int
    Last_Call_Time: int
    Campaning_Data: int
    
    id = db.Column(db.Integer, primary_key=True)
    Campaning_Name = db.Column(db.String(200), unique=True, nullable=False)
    Collection_Pointer = db.Column(db.Integer)
    Buffer_Pointer = db.Column(db.Integer)
    Status = db.Column(db.String(100), nullable=False)
    Attempts = db.Column(db.Integer)
    License_In_Use = db.Column(db.Integer)
    First_Call_Time = db.Column(db.Integer)
    Last_Call_Time = db.Column(db.Integer)
    Campaning_Data = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def __repr__(self):
        return f'<Compani {self.Campaning_Name}>'
        

@app.login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)

@dataclass
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id: int
    user_name: str
    password: str
    is_admin: bool
    created_on: str
    updated_on: str
    
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow,  onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.user_name}>'
    