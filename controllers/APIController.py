from flask import render_template, redirect, url_for, request, abort, jsonify
from flask_login import current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc, or_
from datetime import datetime

import sys

from config import db
from models.Book import Books
from models.Author import Authors


def search():

    query = request.args.get('q')

    if not query:
        abort(404)

    books = Books.query.filter(or_(Books.title.like('%' + query + '%'), Books.original_title.ilike('%' + query + '%'))).order_by(desc('total_rating')).limit(4).all()
    
    search_result = []

    for book in books:
        book_dict = {}
        book_dict['title'] = book.title
        book_dict['author'] = book.authors[0].name
        book_dict['image'] = book.cover_image
        book_dict['read_time'] = book.read_time
        book_dict['rating'] = book.rating
        book_dict['url'] = url_for('book_bp.book_view', book_slug=book.slug)
        search_result.append(book_dict)

    return jsonify(search_result)

def search_author():

    query = request.args.get('q')
    book_title = request.args.get('book_title')

    if not query:
        abort(404)

    authors = Authors.query.filter(or_(Authors.name.ilike('%' + query + '%'), Authors.original_name.ilike('%' + query + '%'))).order_by(asc('name')).limit(10).all()

    search_result = []

    if book_title:
        book_author = Books.query.filter_by(title=book_title).first().authors[0]
        author_dict = {}
        author_dict['name'] = book_author.name
        author_dict['original_name'] = book_author.original_name
        author_dict['is_book_author'] = True
        search_result.append(author_dict)

    for author in authors:
        if book_title and author.original_name == book_author.original_name:
            continue
        author_dict = {}
        author_dict['name'] = author.name
        author_dict['original_name'] = author.original_name
        author_dict['is_book_author'] = False
        search_result.append(author_dict)

    return jsonify(search_result)