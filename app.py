from flask import *

from surveys import *

from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.debug = True

responses = []

@app.route('/')
def showHome():
  return render_template('home.html', surveys=surveys)

@app.route('/survey/<survey_id>')
def showSurvey(survey_id):
  return render_template('survey.html', survey = surveys.get(survey_id), survey_id = survey_id)