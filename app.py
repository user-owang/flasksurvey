from flask import *

from surveys import *

from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'abcdefghijklmnopqrstuvwxyz'



@app.route('/')
def showHome():
  for test in surveys:
    if not session.get(test):
      session[test] = list()
  return render_template('home.html', surveys=surveys)

@app.route('/survey/<survey_id>')
def showSurvey(survey_id):
  if len(session.get(survey_id)) == len(surveys.get(survey_id).questions):
    return redirect(f'/survey/{survey_id}/thanks')
  else:
    return redirect(f'/survey/{survey_id}/question/{len(session.get(survey_id))}')
  return render_template('survey.html', survey = surveys.get(survey_id), survey_id = survey_id)

@app.route('/survey/<survey_id>/question/<int:index>')
def showQuestion(survey_id, index):
  if index < len(session.get(survey_id)):
    redirect(f'/survey/{survey_id}/question/{len(session.get(survey_id))}')
    return flash('You have tried to access questions out of order. Please continue where you left off.')
  if len(surveys[survey_id].questions) == index and len(session.get(survey_id)) == index:
    return redirect(f'/survey/{survey_id}/thanks')
  return render_template('question.html', survey = surveys.get(survey_id), survey_id = survey_id, i = index)

@app.route('/survey/<survey_id>/responses', methods=['POST'])
def addResponse(survey_id):
  answer = request.form['question']
  text = request.form.get('text')
  if text:
    answer = {'answer': request.form['question'], 'text': text}
  temp = session[survey_id]
  temp.append(answer)
  session[survey_id] = temp
  return redirect(f'question/{len(session[survey_id])}')

@app.route('/survey/<survey_id>/thanks')
def showThanks(survey_id):
  return render_template('thanks.html', survey = surveys.get(survey_id), test = survey_id, indexes = list(range(0,len(surveys.get(survey_id).questions))))