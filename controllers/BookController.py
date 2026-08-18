from flask import abort, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from models.Book import Books, Ideas
from models.Category import Categories
from services.bookmarks import BookmarkService
from services.books import BookService


book_service = BookService()
bookmark_service = BookmarkService()


def book_view(book_slug):
    book = book_service.get_by_slug(book_slug)
    if book is None:
        abort(404)
    category_id = book.categories[0].id if book.categories else None
    similar_books = book_service.similar(category_id, 10)
    trending_books = book_service.trending(category_id, 10)
    if current_user.is_authenticated:
        bookmark = bookmark_service.is_bookmarked(current_user.id, book.id)
        return render_template('views/book/book.html', book=book, similar_books=similar_books, trending_books=trending_books, bookmark=bookmark)
    top_links = Books.query.order_by(Books.id.desc()).limit(6).all()
    categories = Categories.query.all()
    ideas = Ideas.query.filter_by(book_id=book.id).order_by(Ideas.order.asc()).all()
    return render_template('views/main/book.html', book=book, ideas=ideas, similar_books=similar_books, trending_books=trending_books, top_links=top_links, categories=categories)


@login_required
def bookmark_view(book_slug):
    book = book_service.get_by_slug(book_slug)
    if book is None:
        abort(404)
    if bookmark_service.is_bookmarked(current_user.id, book.id):
        bookmark_service.remove(current_user.id, book.id, request.remote_addr)
    else:
        bookmark_service.add(current_user.id, book.id, request.remote_addr)
    return redirect(url_for('book_bp.book_view', book_slug=book_slug))


@login_required
def reader_view(book_slug=None, idea=0):
    book, ideas, selected_idea = book_service.get_reader_content(book_slug, idea)
    if book is None or selected_idea is None:
        abort(404)
    return render_template('views/book/reader.html', book=book, ideas=ideas, idea=selected_idea, idea_count=len(ideas) - 1)


@login_required
def bookmark():
    book_id = request.values.get('book_id')
    if not book_id:
        abort(404)
    if request.method == 'POST':
        bookmark_service.add(current_user.id, book_id, request.remote_addr)
    elif request.method == 'DELETE':
        bookmark_service.remove(current_user.id, book_id, request.remote_addr)
    else:
        return jsonify({'status': 'success', 'bookmark': int(bookmark_service.is_bookmarked(current_user.id, book_id))}, 200)
    return jsonify({'status': 'success'}, 200)


# Compatibility query helpers.
def get_book_details_by_slug(slug):
    return book_service.get_by_slug(slug)


def get_similar_books_by_category(category_id, size):
    return book_service.similar(category_id, size)


def get_trending_books_by_category(category_id, size):
    return book_service.trending(category_id, size)


def check_bookmark(book_id, user_id):
    return bookmark_service.is_bookmarked(user_id, book_id)


def add_bookmark(user_id, book_id):
    return bookmark_service.add(user_id, book_id, request.remote_addr)


def remove_bookmark(user_id, book_id):
    return bookmark_service.remove(user_id, book_id, request.remote_addr)


def book_slug_to_id(slug):
    book = book_service.get_by_slug(slug)
    if book is None:
        abort(404)
    return book.id
