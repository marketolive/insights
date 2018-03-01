from flask import Flask, session
from flask_session import Session

app = Flask(__name__)
app.secret_key = '123123'
app.config['SESSION_TYPE'] = 'filesystem'
app.config.from_object('config')
Session(app)

if app.config['FORCE_SSL'] and not app.debug:
  from flask_sslify import SSLify
  sslify = SSLify(app)

from app import views