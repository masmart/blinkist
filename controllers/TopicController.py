
from flask import render_template, redirect, url_for, request, abort
from flask_sqlalchemy import SQLAlchemy

import sys

from models.Topic import Topics


db = SQLAlchemy()

def index():
    return '<h1>some shit</h1>'

def store():
    return '<h1>some shit</h1>'

def show(topic_id):
    pass

def update(topic_id):
    pass

def delete(topic_id):
    pass