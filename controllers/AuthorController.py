
from flask import render_template, redirect, url_for, request, abort
from flask_sqlalchemy import SQLAlchemy

import sys

from models.Author import Authors


db = SQLAlchemy()

def index():
    return render_template('views/author/index.html')

def store():
    return '<h1>some shit</h1>'

def show(author_id):
    pass

def update(author_id):
    pass

def delete(author_id):
    pass