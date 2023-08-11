from database.db import db, mongo
import hashlib
from models.models import User
import re
import random
from datetime import datetime

def encrypt(password):
    ''' SHA256 '''
    hash_pass = hashlib.sha256()
    hash_pass.update(password.encode("utf-8"))
    return str(hash_pass.digest())

def checkAuthentication(ref, uname, password):
    '''user authentication'''
    password = encrypt(password)
    user = db.session.query(User).filter(User.username == uname).first()
    if user == None:
        return False
    if user.password != password:
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

def getDomain(email):
    match = re.findall(r'@[A-Za-z0-9.-]+$', email)
    print(match)
    if match:
        return match[0]
    return None

def newUser(uname,password,email):
    ''' User registration '''
    users = db.session.query(User).all()
    le = len(users)+1
    le = uname[0]+str(int(random.random()*10000000))+str(le)+uname[-1]
    domain = getDomain(email)
    if domain == None:
        return False
    try:
        new_user = User(userid = le, email = email, username = uname, password = encrypt(password), domain = domain)
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
    candidates_data = []
    print(candidates)
    for i in candidates:
        candidates_data.append([i, 0])

    new_poll = {
        'poll_id': poll_id,
        'username': username,
        'startdate': sdate,
        'enddate': edate,
        'candidates': candidates_data,
        'polled': []
    }
    mongo.db.PollingDB.insert_one(new_poll)

def deletePoll(pollid):
    try:
        mongo.db.PollingDB.delete_one({ "poll_id":pollid })
    except:
        return False
    return True

def getAllPolls():
    polls = mongo.db.PollingDB.find()
    print(polls)
    return polls

def getDisplayPolls(uname):
    polls = getAllPolls()
    today = datetime.today()
    today = str(today)
    available_and_eligible = []
    print(today)
    for poll in polls:
        edate = poll['enddate'][:10]
        sdate = poll['startdate'][:10]
        if edate >= today and sdate <= today:
            available_and_eligible.append(poll)
    print(available_and_eligible)
    return available_and_eligible

def getUserPolls(uname):
    print(uname)
    #polls = mongo.db.PollingDB.find({'username':uname})
    polls = getAllPolls()
    userpolls = []
    for i in polls:
        print(i['username'])
        if i['username'] == uname:
            userpolls.append(i)

    print(userpolls)
    return userpolls