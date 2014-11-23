from flask import Flask, redirect, session, request, render_template, url_for, flash, jsonify
from app import app
from api import API

@app.route('/')
def index_view():
  return render_template('index.html')

@app.route('/api/check_auth', methods=['POST'])
def check_auth_view():
  api = API(request.json.get('kerberos'), request.json.get('password'))
  if api.authenticated:
    user =  api.get_user()
  else:
    user = {}
  return jsonify({"authenticated": api.authenticated, "user": user})

@app.route('/api/grades', methods=['POST'])
def get_grades_view():
  api = API(request.json.get('kerberos'), request.json.get('password'))
  if api.authenticated:
    grades =  api.get_grades()
  else:
    grades = {}
  return jsonify({"authenticated": api.authenticated, "grades": grades})
