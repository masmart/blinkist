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

from config import admin, db, ckeditor, MINIO_AUDIO_BUCKET, MINIO_BOOK_COVER_BUCKET
from controllers.UploadContoller import upload_content

from models.User import Users, Bookmarks
from models.Author import Authors
from models.Book import Books, Ideas, Audios, book_authors, book_categories
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

def book_edit_view():

    book_id = request.args.get('id')

    if book_id:
        book = Books.query.filter_by(id=book_id).first()
        categories = Categories.query.with_entities(Categories.id, Categories.name).all()
        ideas = Ideas.query.filter_by(book_id=book_id).order_by(Ideas.order.asc()).all()
        audios = Audios.query.filter_by(book_id=book_id).all()

    if request.method == 'POST':

        book_cover_file = None

        if request.files.get('book-cover-file'):
            book_cover_file = request.files.get('book-cover-file')

        slug = request.form.get('book-slug').replace(' ', '-')
        name = request.form.get('book-title')
        original_name = request.form.get('book-original-title')
        book_category = request.form.get('book-category')
        tagline = request.form.get('tagline')
        book_author = request.form.get('author')
        read_time = request.form.get('read-time')
        description = request.form.get('book-description')
        updated_at = datetime.now()

        if not slug or not name or not original_name or not book_category or not book_author or not read_time or not description:
            return 

        author = Authors.query.filter_by(name=book_author).one()
        category = Categories.query.filter_by(name=book_category).one()

        book.title = name
        book.original_title = original_name
        book.tagline = tagline
        book.tagline_html = tagline
        book.ideas = len(ideas)
        book.type = 'book'
        book.has_audio = False
        book.read_time = read_time
        book.description = description
        book.author_id = book_author
        book.slug = slug
        book.updated_at = updated_at
        book.categories = [category]
        book.authors = [author]

        if book_cover_file:
            book.cover_image = upload_content(book_cover_file, MINIO_BOOK_COVER_BUCKET)

        db.session.add(book)
        db.session.commit()

        return redirect(url_for('admin_bp.books_view'))

    return render_template(template_name_or_list='admin/book_edit.html', book=book, categories=categories, ideas=ideas, audios=audios)

def book_add_view():

    categories = Categories.query.all()

    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        book_cover_file = request.files['book-cover-file']
        name = request.form.get('book-title')
        original_name = request.form.get('book-original-title')
        book_category = request.form.get('book-category')
        tagline = request.form.get('tagline')
        read_time = request.form.get('read-time')
        description = request.form.get('book-description')
        book_author = request.form.get('author')
        slug = name.replace(' ', '-')
        created_at = datetime.now()
        updated_at = created_at

        if not book_cover_file or not name or not original_name or not categories or not tagline or not read_time or not description:
            return

        author = Authors.query.filter_by(name=book_author).one()
        category = Categories.query.filter_by(name=book_category).one()

        book_cover = upload_content(book_cover_file, MINIO_BOOK_COVER_BUCKET)
        book = Books(title=name, original_title=original_name, tagline=tagline, tagline_html=tagline, read_time=read_time, ideas=0, type='book', has_audio=False, description=description, published_at=created_at, cover_image=book_cover, slug=slug, created_at=created_at, updated_at=updated_at)

        db.session.add(book)
        db.session.commit()
        db.session.refresh(book)

        book_author = book_authors.insert().values(book_id=book.id, author_id=author.id)
        book_category = book_categories.insert().values(book_id=book.id, category_id=category.id)

        db.session.execute(book_author)
        db.session.execute(book_category)
        db.session.commit()

        return redirect(url_for('admin_bp.books_view'))
        

    return render_template('admin/book_add.html', categories=categories)

def idea_add_view():

    book_id = request.args.get('book_id')
    book = Books.query.filter_by(id=book_id).first()

    if request.method == 'POST':
        idea = Ideas.query.filter_by(book_id=book_id).order_by(Ideas.id.desc()).first()
        idea_title = request.form.get('idea-title')
        idea_text = request.form.get('idea-text')
        idea_order = idea.order + 1 if idea else 0
        idea_created_at = datetime.now()
        idea_updated_at = idea_created_at

        if not idea_title or not idea_text:
            return 
        
        new_idea = Ideas(title=idea_title, text=idea_text, order=idea_order, book_id=book_id, created_at=idea_created_at, updated_at=idea_updated_at)
        db.session.add(new_idea)
        db.session.commit()

        return redirect(url_for('admin_bp.book_edit_view', id=book_id))

    return render_template('admin/idea_add.html', book=book)

def idea_edit_view():

    book_id = request.args.get('book_id')
    idea_id = request.args.get('id')

    book = Books.query.filter_by(id=book_id).first()
    idea = Ideas.query.filter_by(id=idea_id).first()

    if request.method == 'POST':
        idea_title = request.form.get('idea-title')
        idea_text = request.form.get('idea-text')
        idea_updated_at = datetime.now()

        if not idea_title or not idea_text:
            return

        idea.title = idea_title
        idea.text = idea_text
        idea.updated_at = idea_updated_at

        db.session.add(idea)
        db.session.commit()

        return redirect(url_for('admin_bp.book_edit_view', id=book_id))

    return render_template('admin/idea_edit.html', book=book, idea=idea)

def audio_add_view():

    book_id = request.args.get('book_id')

    book = Books.query.filter_by(id=book_id).first()
    ideas = Ideas.query.filter_by(book_id=book_id).all()

    return render_template('admin/audio_add.html', book=book, ideas=ideas)

def category_view():

    return render_template(template_name_or_list='admin/category.html')

def author_view():

    return render_template(template_name_or_list='admin/author.html')

def report_view():

    return render_template(template_name_or_list='admin/report.html')


