from database.db import db, mongo
import hashlib
from models.models import User
import re
import random

def encrypt(password):
    ''' ShA256 '''
    hash_pass = hashlib.sha256()
    hash_pass.update(password.encode("utf-8"))
    return str(hash_pass.digest())

def checkAuthentication(ref, uname, password):
    '''user authentication'''
    password = encrypt(password)
    user = db.session.query(User).filter(User.username == uname, User.password == password).first()
    if user == None:
        return False
    return True

def validateInput(uname,email,password,confirm):
    if len(uname) == 0 or len(email) == 0 or len(password) == 0 or len(confirm) == 0:
        return 'Please fill all the fields'
    if password != confirm:
        return 'Password must match with confirm password'
    if len(password) < 8:
        return 'Length of password must be greater than or equal to 8'
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.fullmatch(regex,email):
        return 'Enter valid email'
    return 'true'

def newUser(uname,password,email):
    ''' User registration '''
    users = db.session.query(User).all()
    le = len(users)+1
    try:
        new_user = User(user_id = le, username = uname, email = email, password = encrypt(password))
        db.session.add(new_user)
        db.session.commit()
    except:
        return False
    else:
        return True

# Poll helpers
def newPoll(candidates, username, sdate, edate):
    poll_id = int(random.random()*10000000)+random.randint(1,100)
    poll_id = username[0]+str(poll_id)+username[-1]
    