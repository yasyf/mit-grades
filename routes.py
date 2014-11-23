from flask import session, request, render_template, jsonify, g
from app import app
from api import API
import uuid

@app.before_request
def preprocess_request():
  if not session.get('uuid'):
    session['uuid'] = str(uuid.uuid4())
  g.api = API.get_api(session['uuid'])
  if request.json and 'kerberos' in request.json and 'password' in request.json:
    if not g.api or not g.api.match(request.json.get('kerberos'), request.json.get('password')):
      g.api = API(session['uuid'], request.json.get('kerberos'), request.json.get('password'))

@app.route('/')
def index_view():
  return render_template('index.html')

@app.route('/api/check_auth', methods=['POST'])
def check_auth_view():
  if g.api.authenticated:
    user =  g.api.get_user()
  else:
    user = {}
  return jsonify({"authenticated": g.api.authenticated, "user": user})

@app.route('/api/grades', methods=['POST'])
def get_grades_view():
  if g.api.authenticated:
    grades =  g.api.get_grades()
  else:
    grades = {}
  return jsonify({"authenticated": g.api.authenticated, "grades": grades})
