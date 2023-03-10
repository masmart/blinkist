
from flask import render_template, redirect, url_for, request, abort, jsonify
from flask_login import current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, asc
from datetime import datetime

import sys

from config import db
from models.Book import Books, Ideas, Audios
from models.User import Bookmarks
from models.Category import Categories


def book_view(book_slug):

    book = get_book_details_by_slug(book_slug)

    similar_books = get_similar_books_by_category(book.categories[0].id, 10)
    trending_books = get_trending_books_by_category(book.categories[0].id, 10)
    bookmark = check_bookmark(book.id, current_user.id)

    return render_template('views/book/book.html', book=book, similar_books=similar_books, trending_books=trending_books, bookmark=bookmark)

@login_required
def bookmark_view(book_slug):

    book_id = book_slug_to_id(slug=book_slug)
    user_id = current_user.id

    if not check_bookmark(book_id, user_id):
        add_bookmark(user_id, book_id)
    else:
        remove_bookmark(user_id, book_id)

    return redirect(location=url_for('book_bp.book_view', book_slug=book_slug))

@login_required
def reader_view(book_slug=None, idea=0):


    book = Books.query.filter_by(slug=book_slug).first()
    ideas = Ideas.query.filter_by(book_id=book.id).order_by(asc(Ideas.order)).all()
    idea = Ideas.query.filter_by(book_id=book.id, order=idea).one()
    idea_count = len(ideas) - 1
    
    return render_template('views/book/reader.html', book=book, ideas=ideas, idea=idea, idea_count=idea_count)

def bookmark():

    user_id = request.form.get('user_id')
    book_id = request.form.get('book_id')

    if not user_id or not book_id:
        abort(404)

    if request.method == 'POST':
        add_bookmark(user_id, book_id)
    elif request.method == 'DELETE':
        delete_bookmark(user_id, book_id)
    elif request.method == 'GET':
        if check_bookmark(book_id, user_id):
            return jsonify({'status': 'success', 'bookmark': 1}, 200)
        else:
            return jsonify({'status': 'success', 'bookmark': 0}, 200)

    return jsonify({'status': 'success'}, 200)

def get_book_details_by_slug(slug):

    book = Books.query.filter_by(slug=slug).first()
    
    return book

def get_similar_books_by_category(category_id, size):
    
    books = Books.query.join(Books.categories).filter(Categories.id == category_id).order_by(Books.rating.asc()).limit(size).all()

    return books

def get_trending_books_by_category(category_id, size):
    
    books = Books.query.join(Books.categories).filter(Categories.id == category_id).order_by(Books.total_rating.asc()).limit(size).all()

    return books

def check_bookmark(book_id, user_id):

    bookmark = Bookmarks.query.filter_by(book_id=book_id, user_id=user_id, deleted_at=None).first()

    if bookmark is not None:
        return True
    else:
        return False

def add_bookmark(user_id, book_id):

    now = datetime.now()
    ip = request.remote_addr

    bookmark = Bookmarks(user_id=user_id, book_id=book_id, created_at=now, creator_ip=ip, updated_at=now, updater_ip=ip)
    db.session.add(bookmark)
    db.session.commit()

def remove_bookmark(user_id, book_id):

    now = datetime.now()
    ip = request.remote_addr

    try:
        bookmark = Bookmarks.query.filter_by(book_id=book_id, user_id=user_id, deleted_at=None).first()
        bookmark.deleted_at = now
        bookmark.deletor_ip = ip
        db.session.commit()
    except:
        return False

    return True

def book_slug_to_id(slug):

    book = Books.query.filter_by(slug=slug).first()

    return book.id