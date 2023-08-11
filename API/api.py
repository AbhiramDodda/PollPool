from flask_restful import Resource
from database.db import mongo, db
from Helpers.helpers import newPoll, deletePoll
from flask import request, redirect, make_response, render_template, session

class CreatePoll(Resource):
    def get(self):
        pass
    def put(self):
        pass
    def post(self):
        candidates_list, uname, sdate, edate = request.get_json()['data'], request.get_json()['username'], request.get_json()['startdate'], request.get_json()['enddate']
        print(candidates_list, uname, sdate, edate)
        if(newPoll(candidates_list, uname, sdate, edate)):
            return redirect('/userdashboard')
        return make_response(render_template("error.html", link="/"))
    def delete(self):
        pass

class DeletePoll(Resource):
    def get(self):
        pass
    def put(self):
        pass
    def post(self):
        choice = request.form['choice']
        pollid = request.form['pollid']
        if choice == 'no':
            return make_response(render_template('/userdashboard'))
        if(deletePoll(pollid)):
            return redirect('/userdashboard')
        return make_response(render_template("error.html", link="/"))
    def delete(self):
        pass