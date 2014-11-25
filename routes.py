from flask import session, request, render_template, jsonify, g, redirect
from app import app, dev
from api import API
import uuid

@app.before_request
def preprocess_request():
  if not session.get('uuid'):
    session['uuid'] = str(uuid.uuid4())
  g.api = API.get_api(session['uuid'])
  if request.json and 'kerberos' in request.json and 'password' in request.json:
    if not g.api or not g.api.match(request.json['kerberos'], request.json['password']):
      g.api = API(session['uuid'], request.json['kerberos'], request.json['password'])

@app.after_request
def postprocess_request(response):
  if not dev:
    response.headers.setdefault('Strict-Transport-Security', 'max-age=31536000')
    if not request.is_secure:
      return redirect(request.url.replace('http://', 'https://', 1), code=301)
  return response

@app.route('/')
def index_view():
  return render_template('index.html')

@app.route('/api/check_auth', methods=['POST'])
def check_auth_view():
  if g.api.authenticated:
    user = g.api.get_user()
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
