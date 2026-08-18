from flask import request, render_template, redirect, url_for
from sqlalchemy import asc, desc, or_
from flask_paginate import Pagination, get_page_args
from datetime import datetime

from config import admin, db, MINIO_AUDIO_BUCKET, MINIO_BOOK_COVER_BUCKET
from controllers.UploadContoller import upload_content

from models.User import Users, Bookmarks
from models.Author import Authors
from models.Book import Books, Ideas, Audios, book_authors, book_categories
from models.Collection import Collections, Curators
from models.Category import Categories
from models.Topic import Topics


def dashboard_view():

    return render_template(template_name_or_list='admin/dashboard.html')

def books_view():

    query = request.args.get('q')

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')

    if query:
        books = Books.query.filter(or_(Books.title.like('%' + query + '%'), Books.original_title.ilike('%' + query + '%'))).order_by(Books.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    else:
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
        wsr_1 = request.form.get('who-should-read-1')
        wsr_2 = request.form.get('who-should-read-2')
        wsr_3 = request.form.get('who-should-read-3')
        best_quote = request.form.get('best-quote')
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
        book.who_should_read_1 = wsr_1
        book.who_should_read_2 = wsr_2
        book.who_should_read_3 = wsr_3
        book.best_quote = best_quote
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
        wsr_1 = request.form.get('who-should-read-1')
        wsr_2 = request.form.get('who-should-read-2')
        wsr_3 = request.form.get('who-should-read-3')
        best_quote = request.form.get('best-quote')
        book_author = request.form.get('author')
        slug = name.replace(' ', '-')
        created_at = datetime.now()
        updated_at = created_at

        if not book_cover_file or not name or not original_name or not categories or not tagline or not read_time or not description:
            return

        author = Authors.query.filter_by(name=book_author).one()
        category = Categories.query.filter_by(name=book_category).one()

        book_cover = upload_content(book_cover_file, MINIO_BOOK_COVER_BUCKET)
        book = Books(title=name, original_title=original_name, tagline=tagline, tagline_html=tagline, read_time=read_time, ideas=0, type='book', has_audio=False, description=description, who_should_read_1=wsr_1, who_should_read_2=wsr_2, who_should_read_3=wsr_3, best_quote=best_quote, published_at=created_at, cover_image=book_cover, slug=slug, created_at=created_at, updated_at=updated_at)

        db.session.add(book)
        db.session.flush()

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
        idea_sample_text = request.form.get('sample-idea-text')
        idea_order = idea.order + 1 if idea else 0
        idea_created_at = datetime.now()
        idea_updated_at = idea_created_at

        if not idea_title or not idea_text:
            return 
        
        new_idea = Ideas(title=idea_title, text=idea_text, sample_text=idea_sample_text, order=idea_order, book_id=book_id, created_at=idea_created_at, updated_at=idea_updated_at)
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
        idea_sample_text = request.form.get('sample-idea-text')
        idea_updated_at = datetime.now()

        if not idea_title or not idea_text:
            return

        idea.title = idea_title
        idea.text = idea_text
        idea.sample_text = idea_sample_text
        idea.updated_at = idea_updated_at

        db.session.add(idea)
        db.session.commit()

        return redirect(url_for('admin_bp.book_edit_view', id=book_id))

    return render_template('admin/idea_edit.html', book=book, idea=idea)

def audio_add_view():

    book_id = request.args.get('book_id')

    book = Books.query.filter_by(id=book_id).first()
    ideas = Ideas.query.filter_by(book_id=book_id).all()

    if request.method == 'POST':
        audio_title = request.form.get('audio-title')
        audio_sample_file = request.files['audio-sample-file']
        audio_file = request.files['audio-file']
        audio_created_at = datetime.now()
        audio_updated_at = audio_created_at

        if not audio_title or not audio_sample_file or not audio_file:
            return
        
        ideas = Ideas.query.filter_by(book_id=book_id, title=audio_title).one()

        idea_id = ideas.id
        audio_order = ideas.order

        audio_sample = upload_content(audio_sample_file, MINIO_AUDIO_BUCKET)
        audio = upload_content(audio_file, MINIO_AUDIO_BUCKET)

        new_audio = Audios(book_id=book_id, file=audio, sample_file=audio_sample, order=audio_order, created_at=audio_created_at, updated_at=audio_updated_at, idea_id=idea_id)

        db.session.add(new_audio)
        db.session.commit()

        return redirect(url_for('admin_bp.book_edit_view', id=book_id))

    return render_template('admin/audio_add.html', book=book, ideas=ideas)

def audio_edit_view():

    book_id = request.args.get('book_id')
    audio_id = request.args.get('id')

    book = Books.query.filter_by(id=book_id).first()
    audio = Audios.query.filter_by(id=audio_id).first()
    ideas = Ideas.query.filter_by(book_id=book_id).all()

    return render_template('admin/audio_edit.html', book=book, ideas=ideas, audio=audio)

def report_view():

    return render_template(template_name_or_list='admin/report.html')


from controllers.AdminTaxonomyController import (
    author_add_view,
    author_edit_view,
    authors_view,
    categories_view,
    category_add_view,
    category_edit_view,
)


