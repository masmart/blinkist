from flask import request, render_template, redirect, url_for
from flask_paginate import Pagination, get_page_args
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, DateField, FileField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, InputRequired
from wtforms.widgets import TextArea
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash
from datetime import datetime
import warnings

from config import admin, db, ckeditor

from models.User import Users, Bookmarks
from models.Author import Authors
from models.Book import Books, Ideas, Audios
from models.Collection import Collections, Curators
from models.Category import Categories
from models.Topic import Topics


class UserView(ModelView):
    page_size = 20
    can_delete = False
    column_exclude_list=['first_name', 'last_name', 'password', 'session_token', 'updated_at', 'updater_ip', 'deleted_at', 'deletor_ip']
    column_searchable_list=['first_name', 'last_name', 'email', 'full_name']

    def on_model_change(self, form, model, is_created):
        model.password = generate_password_hash(model.password, method='SHA256')


class BookView(ModelView):
    page_size = 20
    can_delete = False
    column_exclude_list=['tagline', 'tagline_html', 'read_time', 'ideas', 'type', 'has_audio', 'description', 'rating', 'total_rating', 'cover_image', 'purchase_url', 'slug', 'updated_at', 'deleted_at']
    column_searchable_list=['title', 'slug', 'original_title']


class IdeasView(ModelView):
    page_size = 20
    can_delete = False
    column_exclude_list=['created_at', 'updated_at', 'deleted_at']
    form_create_rules = ['idea_book', 'title', 'text', 'order']
    form_edit_rules = ['idea_book', 'title', 'text', 'order']
    column_searchable_list=['title', 'idea_book.title', 'idea_book.original_title']

    def on_model_change(self, form, model, is_created):
        now = datetime.now()
        model.created_at = now
        model.updated_at = now


class CollectionView(ModelView):
    page_size = 20
    can_delete = False
    column_exclude_list=['tagline', 'cover_image', 'created_at', 'updated_at', 'deleted_at']
    column_searchable_list=['name', 'original_name', 'curators.name', 'curators.users.full_name', 'curators.users.email']
    form_create_rules = ['curators', 'categories', 'original_name', 'name', 'tagline', 'description', 'cover_image', 'books']
    form_edit_rules = ['curators', 'categories', 'original_name', 'name', 'tagline', 'description', 'cover_image', 'books']

    def on_model_change(self, form, model, is_created):
        now = datetime.now()
        model.slug = model.name.replace(' ', '-')
        model.created_at = now
        model.updated_at = now


class CuratorView(ModelView):
    page_size = 20
    can_delete = False
    column_exclude_list=['avatar', 'created_at', 'updated_at', 'deleted_at']
    column_searchable_list=['name', 'users.full_name', 'users.email']
    form_create_rules = ['name', 'avatar', 'users']
    form_edit_rules = ['name', 'avatar', 'users']

    def on_model_change(self, form, model, is_created):
        now = datetime.now()
        model.created_at = now
        model.updated_at = now


def init():
    
    admin.name = 'کتابچ'
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', 'Fields missing from ruleset', UserWarning)
        admin.add_view(UserView(Users, db.session))
        admin.add_view(BookView(Books, db.session))
        admin.add_view(CollectionView(Collections, db.session))
        admin.add_view(CuratorView(Curators, db.session))
        admin.add_view(IdeasView(Ideas, db.session))

    admin.add_view(ModelView(Audios, db.session))
    admin.add_view(ModelView(Categories, db.session))
    admin.add_view(ModelView(Topics, db.session))
    admin.add_view(ModelView(Authors, db.session))
    admin.add_view(ModelView(Bookmarks, db.session))


def dashboard_view():

    return render_template(template_name_or_list='admin/dashboard.html')

def books_view():

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')

    books = Books.query.filter().order_by(Books.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    pagination = Pagination(page=page, per_page=per_page, total=books.total)

    return render_template(template_name_or_list='admin/books.html', books=books, page=page, per_page=per_page, pagination=pagination)

def book_view():

    book_id = request.args.get('id')

    if book_id:
        book = Books.query.filter_by(id=book_id).first()
        categories = Categories.query.with_entities(Categories.id, Categories.name).all()
        authors = Authors.query.with_entities(Authors.id, Authors.name).all()
        ideas = Ideas.query.filter_by(book_id=book_id).all()
        audios = Audios.query.filter_by(book_id=book_id).all()

    return render_template(template_name_or_list='admin/book_view.html', book=book, categories=categories, ideas=ideas, audios=audios)

def idea_add_view():

    book_id = request.args.get('book_id')
    book = Books.query.filter_by(id=book_id).first()

    return render_template('admin/idea_add.html', book=book)

def idea_edit_view():

    book_id = request.args.get('book_id')
    idea_id = request.args.get('id')

    book = Books.query.filter_by(id=book_id).first()
    idea = Ideas.query.filter_by(id=idea_id).first()

    print(idea.title)

    return render_template('admin/idea_edit.html', book=book, idea=idea)


def category_view():

    return render_template(template_name_or_list='admin/category.html')

def author_view():

    return render_template(template_name_or_list='admin/author.html')

def report_view():

    return render_template(template_name_or_list='admin/report.html')


