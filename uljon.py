# uljon.py
from flask import Flask, render_template, redirect, request
from celery import Celery
from os import listdir
from os.path import isfile, join, dirname, abspath 
from sys import path
path.append(dirname(abspath(__file__)) + '/lib')
import generator as Gen

app = Flask(__name__)

@app.route('/')
def index():
	mypath = dirname(abspath(__file__)) + "/txt/"
	files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	return render_template('index.html', files=files) 

@app.route('/generate', methods=['POST'])
def generate():
	# Need error handling for unexpected inputs
	myfile = dirname(abspath(__file__)) + "/txt/" + request.form['file']
	gen = Gen.Generator(myfile)
	sentence = gen.makeSentence(int(request.form['length']))
	print(sentence)
	return redirect('/', 302)
