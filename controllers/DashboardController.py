from flask import render_template, redirect, url_for, request, abort
from flask_login import current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, asc
from datetime import datetime
from random import randrange

import sys
import os

from config import db, login_manager
from models.Book import Books
from models.Category import Categories
from models.User import Users, Bookmarks
from models.Collection import Collections, Curators

@login_required
def dashboard_view():
    
    last_reads = get_last_reads(4)
    promoted = get_last_reads(1)
    recommended = get_last_reads(20)
    collections = Collections.query.order_by(asc(Collections.created_at)).limit(10).all()

    return render_template('views/dashboard/dashboard.html', last_reads=last_reads, promoted=promoted, recommended=recommended, collections=collections)

@login_required
def explore_view():

    recommended = get_last_reads(20)
    categories = get_categories()
    latest = get_last_book(20)
    collections = Collections.query.order_by(asc(Collections.created_at)).limit(10).all()

    return render_template('views/dashboard/explore.html', recommended=recommended, categories=categories, latest=latest, collections=collections)

@login_required
def library_view():
    
    last_reads = get_last_reads(4)
    bookmarked = get_user_bookmarks(user_id=current_user.id)
    finished = get_last_reads(12)

    return render_template('views/dashboard/library.html', last_reads=last_reads, bookmarked=bookmarked, finished=finished)

@login_required
def highlight_view():
        
    return render_template('views/dashboard/highlight.html')

@login_required
def bookmarked_view(page=1):    

        root_dir = url_for('dashboard_bp.library_view')

        view = 'bookmark'
        books = get_user_bookmarks(user_id=current_user.id, page=page, size=20)
        pagination = int(books.total / 20)

        return render_template('views/dashboard/serp.html', view=view, items=books, pagination=pagination, root_dir=root_dir)

@login_required
def finished_view():

    root_dir = url_for('dashboard_bp.library_view')

    view = 'finished'
    books = get_books_by_offset(0, 20)
    pagination = int(books.total / 20)

    return render_template('views/dashboard/serp.html', view=view, items=books, pagination=pagination, root_dir=root_dir)

def get_last_reads(items):

    result = Books.query.filter(Books.id < randrange(1000)).order_by(Books.id.desc()).limit(items).all()

    return result

def get_categories():

    result = Categories.query.order_by(asc(Categories.name)).all()

    return result

def get_last_book(items):

    result = Books.query.filter().order_by(Books.id.desc()).limit(items).all()

    return result

def get_books_by_offset(offset, limit):

    result = Books.query.filter().order_by(Books.id.asc()).paginate(page=offset, per_page=limit, error_out=False)

    return result

def get_count_of_books():

    result = Books.query.count()

    return result

def get_count_of_bookmarks(user_id):

    result = Bookmarks.query.filter_by(user_id=user_id, deleted_at=None).count()

    return result

def get_user_bookmarks(user_id, page=1, size=10):

    bookmarks = Books.query.join(Bookmarks).filter(Bookmarks.user_id == user_id, Bookmarks.deleted_at == None).order_by(desc(Bookmarks.updated_at)).paginate(page=page, per_page=size, error_out=False)

    return bookmarks