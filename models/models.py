from database.db import db
from flask_sqlalchemy import *

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, autoincrement = True)
    email = db.Column(db.String(200), nullable = False)
    username = db.Column(db.String(30),primary_key = True)
    password = db.Column(db.String, nullable = False)