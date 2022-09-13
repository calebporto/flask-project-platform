from json import loads
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Float, DateTime
from sqlalchemy.orm import declarative_base, relationship
from flask_login import UserMixin
from app.models.basemodels import Get_User, User_Loader
from app import login_manager
from app.config import API_URL
import requests


Base = declarative_base()

@login_manager.user_loader
def load_user(user_id):
    send = Get_User(id=user_id)
    response = requests.post(f'{API_URL}/get-user', send.json()).text
    user = User_Loader(**loads(response))
    return User(user.id, user.name, user.email, user.hash, user.is_admin, user.is_designer)

class User(Base, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hash = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    is_designer = Column(Boolean, default=False)

    def __init__(self, id, name, email, hash, is_admin=False, is_designer=False):
        self.id = id
        self.name = name
        self.email = email
        self.hash = hash
        self.is_admin = is_admin
        self.is_designer = is_designer

    def __repr__(self):
        return f'Pessoa({self.name})'