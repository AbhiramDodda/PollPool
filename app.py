from flask import Flask, session, render_template, request, redirect, url_for
import os
from Helpers.helpers import checkAuthentication, validateInput, newUser
from flask_security import Security
from database.db import mongo, db
from flask_restful import Api
from API.api import CreatePoll



def create_app():
    app = Flask(__name__) 
    app.config['MONGO_URI'] = "mongodb+srv://abhiramdodda:AbhiramMongoDB9@cluster0.j0flmnk.mongodb.net/PollDB?retryWrites=true&w=majority"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///D:\Web\PollingApp\database\database.sqlite3"
    mongo.init_app(app)
    db.init_app(app)
    api = Api(app)
    app.secret_key = os.urandom(24)
    return app, api

app, api = create_app()
secure = Security(app)


# Routes
@app.route('/')
def index():
    return render_template("home.html")

@app.route('/logout')
def logout():
    return render_template("home.html")

@app.route('/login',methods=['POST'])
def userlogin():
    if request.method == 'POST' and request.form['username'] != None and request.form['password'] != None:
        username = request.form['username']
        password = request.form['password']
        if checkAuthentication('user',username,password):
            session['user'] = username
            return redirect(url_for('userdashboard'))
        return render_template("error.html", message="Invalid credentials", link = '/user', where = "Login again")

@app.route('/signup')
def userregister():
    return render_template('userregistration.html')

@app.route('/userregistration',methods=['GET','POST'])
def userregistration():
    if request.method == 'POST':
        uname = request.form['username']
        email = request.form['email']
        password=request.form['password']
        confirm_pass = request.form['confirm_password']
        result = validateInput(uname,email,password,confirm_pass)
        if  result == 'true':
            if newUser(uname,password,email):
                session['user'] = uname
                return redirect(url_for('userdashboard'))
            return render_template("error.html", message="Username exists", link = '/userregister', where = "Go back")
        return render_template("error.html", message = result, link = '/userregister', where = "Go back")

@app.route('/<string:user_id>/create_poll')
def create_poll(user_id):
    return render_template('createpoll.html', username = user_id)

@app.route('/userdashboard')
def userdashboard():
    return render_template("userdashboard.html", user_id = session['user'])


api.add_resource(CreatePoll,'/pollapi/create')

if __name__ == '__main__':
    app.run()