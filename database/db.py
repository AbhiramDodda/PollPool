from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy


mongo = PyMongo()

engine = None
db = SQLAlchemy()