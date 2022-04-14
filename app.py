#M. Galih Fikransyah - 19090074
#Muhamad Zaim Zamzami - 19090036
#Fatimatuzzahro - 19090039
#Nirvanna Indiranjani - 19090046
import os
import random
import string
from flask import Flask, render_template, request, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
project_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(os.path.join(project_dir, "database.db"))

db = SQLAlchemy(app)

class  User(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=True, nullable=False)
    def __repr__(self):
        return '<User %r>' % self.username

class  Event(db.Model):
    id_event = db.Column(db.Integer, primary_key=True)
    event_creator = db.Column(db.String(20), unique=True, nullable=False)
    event_name = db.Column(db.String(20), unique=True, nullable=False)
    event_start_time = db.Column(db.DateTime, nullable=True)
    event_end_time = db.Column(db.DateTime, nullable=True)
    event_start_lat = db.Column(db.String(20), unique=True, nullable=False)
    event_finish_lat = db.Column(db.String(20), unique=True, nullable=False)
    event_start_lng = db.Column(db.String(20), unique=True, nullable=False)
    event_finish_lng = db.Column(db.String(20), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Log(db.Model):
    id_log = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    event_name = db.Column(db.String(20), unique=True, nullable=False)
    log_lat = db.Column(db.String(20), unique=True, nullable=False)
    log_lng = db.Column(db.String(20), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

db.create_all()

@app.route("/api/v1/users/create", methods=['POST'])
def createUser():
    newUser = User(username = request.form['username'],password = request.form['password'])

    db.session.add(newUser)
    db.session.commit()

    return jsonify({'msg': 'Registrasi Sukses'}), 200

# login
@app.route("/api/v1/uses/login", methods=['POST'])
def login():
    req = request.json;
    search = User.query.filter_by(username = req['username'], password = req['password']).first();
    if search:
        token = ''.join(random.choises(
            string.ascii_uppercase + string.digits, k=10
        ))

        User.query.filter_by(username = req['username'], password= req['password']).update({token:token});
        db.session.commit();

        return {
            "msg" : "Login Sukses",
            "Token" : token
        }, 200

@app.route("/api/v1/events/create", methods=['POST'])
def createEvent():
    newEvent = Event(
        event_creator = request.form['event_creator'],
        event_name = request.form['event_name'],
        event_start_time = request.form['event_start_time'],
        event_end_time = request.form['event_end_time'],
        event_start_lat = request.form['event_start_lat'],
        event_start_lng = request.form['event_start_lng'],
        event_finish_lat = request.form['event_finish_lat'],
        event_finish_lng = request.form['event_finish_lng']
    )

    db.session.add(newEvent)
    db.session.commit()

    return jsonify({'msg': 'Membuat event sukses'}), 200

@app.route("/api/v1/events/logs", methods=['POST'])
def createEvent():
    newLog = Log(
        event_name = request.form['event_name'],
        log_lat = request.form['log_lat'],
        log_lng = request.form['log_lng']
    )

    db.session.add(newLog)
    db.session.commit()

    return jsonify({'msg': 'Sukses mencatat posisi terbaru'}), 200

@app.route("/api/v1/events/logs", methods=['GET'])
def createEvent():
    db.session.query(User).filter_by(event_name=event_name)

    return jsonify({'msg': 'Sukses mencatat posisi terbaru'}), 200
