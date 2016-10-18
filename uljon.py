# uljon.py
from flask import Flask, render_template
from celery import Celery

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html') # pass in data here as second argument
