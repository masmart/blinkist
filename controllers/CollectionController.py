from flask import render_template, redirect, url_for, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required
from datetime import datetime
import sys

from config import db, login_manager
from models.Collection import Collections, Curators
from models.Book import Books
from models.Category import Categories


def collection_view(slug=None):

    collection = Collections.query.filter_by(slug=slug).first()
    similar_collections = Collections.query.join(Collections.categories).filter(Categories.id == collection.categories[0].id).order_by(Collections.created_at.asc()).limit(10).all()

    return render_template('views/collection/collection.html', collection=collection, similar_collections=similar_collections)