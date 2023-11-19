from flask import *

from surveys import *

from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.debug = True

responses = dict()

@app.route('/')
def showHome():
  return render_template('home.html', surveys=surveys)

@app.route('/survey/<survey_id>')
def showSurvey(survey_id):
  return render_template('survey.html', survey = surveys.get(survey_id), survey_id = survey_id)

@app.route('/survey/<survey_id>/question/<int:index>')
def showQuestion(survey_id, index):
  if responses.get(survey_id) and index > len(responses.get(survey_id)):
    redirect(f'/survey/{survey_id}/question/{len(responses.get(survey_id))}')
    return flash('You have tried to access questions out of order. Please continue where you left off.')  
  if not responses.get(survey_id) and index>0:
    redirect(f'/survey/{survey_id}/question/0')
    return flash('You have tried to access questions out of order. Please continue where you left off.')
  if len(surveys.get(survey_id)['questions']) == index and responses.get(survey_id) and len(responses.get(survey_id)) == index:
    return redirect('/thanks')
  return render_template('question.html', survey = surveys.get(survey_id), survey_id = survey_id, i = index)

@app.route('/survey/<survey_id>/responses', methods=['POST'])
def addResponse(survey_id):
  answer = request.form['question']
  text = request.form.get('text')
  if not responses.get(survey_id):
    responses[survey_id] = []
  if text:
    answer = {'answer': request.form['question'], 'text': text}
  responses[survey_id].append(answer)
  return redirect(f'question/{len(responses[survey_id])}')

@app.route('/thanks')
def showThanks():
  return render_template('thanks.html')