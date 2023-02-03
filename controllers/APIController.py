from flask import render_template, redirect, url_for, request, abort, jsonify
from flask_login import current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, or_
from datetime import datetime

import sys

from config import db
from models.Book import Books


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