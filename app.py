from flask import flask, request, render_template

from surveys import *

from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

responses = []

app.route('/')
def showHome():
  