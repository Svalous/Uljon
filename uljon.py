# uljon.py
from flask import Flask, render_template, redirect, request
from celery import Celery
import praw
from os import listdir
from os.path import isfile, join, dirname, abspath 
from sys import path
path.append(dirname(abspath(__file__)) + '/lib')
import generator as Gen
import secrets as s

# Celery helper function
def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery('/')

# Flask Init / Celery integration
app = Flask(__name__)
app.config.update(
        CELERY_BROKER_URL='redis://localhost:6379',
        CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(app)

# Celery tasks
@celery.task()
def post(file_name, file_path, length):
    # TODO: Error Checking if sentence > 300 characters, put sentence in arg text=sentence
    gen = Gen.Generator(file_path)
    gen.makeChain()
    sentence = gen.makeSentence(length)
    # Post to reddit
    r.submit('uljon', '[{0}]'.format(file_name) + sentence, text='')
    return

def index():
	link_refresh = r.get_authorize_url('KeepThePartyAlive', 'submit', refreshable=True)
	return render_template('index.html', refresh = link_refresh) 

@app.route('/authorize_callback', methods=['GET', 'POST'])
def authorized():
	text_path = dirname(abspath(__file__)) + "/txt/"
	files = [f for f in listdir(text_path) if isfile(join(text_path, f))]
	if request.method == 'GET':
		state = request.args.get('state', '')
		code = request.args.get('code', '')
		access_information= r.get_access_information(code)
		return render_template('authorize_callback.html', files=files)
	elif request.method == 'POST':
		file_path = text_path + request.form['file']
                # Start celery background task to post
                post.delay(request.form['file'], file_path, int(request.form['length']))
                post.wait()
		return render_template('authorize_callback.html', files=files)

if __name__ == '__main__':
	r = praw.Reddit('Random sentence generator by u/Uljon ver 0.1')
	r.set_oauth_app_info(s.CLIENT_ID, s.CLIENT_SECRET, s.REDIRECT_URI)
	app.run(debug=True, port=65010)
