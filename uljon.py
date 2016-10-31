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

app = Flask(__name__)

# put the below in a seperate file and .gitignore it

@app.route('/')
def index():
	link_refresh = r.get_authorize_url('KeepThePartyAlive', 'submit', refreshable=True)
	return render_template('index.html', refresh = link_refresh) 

@app.route('/authorize_callback', methods=['GET', 'POST'])
def authorized():
	mypath = dirname(abspath(__file__)) + "/txt/"
	files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	if request.method == 'GET':
		state = request.args.get('state', '')
		code = request.args.get('code', '')
		access_information= r.get_access_information(code)
		return render_template('authorize_callback.html', files=files)
	elif request.method == 'POST':
		myfile = dirname(abspath(__file__)) + "/txt/" + request.form['file']
		gen = Gen.Generator(myfile)
		gen.makeChain()
		sentence = gen.makeSentence(int(request.form['length']))
		# Post to reddit
		# TODO: Error Checking if sentence > 300 characters, put sentence in arg text=sentence
		r.submit('uljon', '[{0}] '.format(request.form['file']) + sentence, text='')
		return render_template('authorize_callback.html', files=files)

if __name__ == '__main__':
	r = praw.Reddit('Random sentence generator by u/Uljon ver 0.1')
	r.set_oauth_app_info(s.CLIENT_ID, s.CLIENT_SECRET, s.REDIRECT_URI)
	app.run(debug=True, port=65010)
