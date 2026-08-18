from datetime import datetime

from flask import redirect, render_template, request, url_for
from flask_paginate import Pagination, get_page_args

from config import db
from models.Author import Authors
from models.Category import Categories


def categories_view():
    page, per_page, _ = get_page_args(page_parameter='page', per_page_parameter='per_page')
    categories = Categories.query.order_by(Categories.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    pagination = Pagination(page=page, per_page=per_page, total=categories.total)
    return render_template('admin/categories.html', categories=categories, page=page, per_page=per_page, pagination=pagination)


def category_add_view():
    if request.method == 'POST':
        name = request.form.get('name')
        original_name = request.form.get('original-name')
        description = request.form.get('description')
        icon = request.form.get('icon')
        if not name or not original_name or not description or not icon:
            return render_template('admin/category_add.html')
        now = datetime.now()
        category = Categories(name=name, original_name=original_name, description=description, icon=icon, slug=name.replace(' ', '-'), created_at=now, updated_at=now)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('admin_bp.categories_view'))
    return render_template('admin/category_add.html')


def category_edit_view():
    category = Categories.query.filter_by(id=request.args.get('id')).first_or_404()
    if request.method == 'POST':
        name = request.form.get('name')
        original_name = request.form.get('original-name')
        description = request.form.get('description')
        icon = request.form.get('icon')
        if not name or not original_name or not description or not icon:
            return render_template('admin/category_edit.html', category=category)
        category.name = name
        category.original_name = original_name
        category.description = description
        category.icon = icon
        category.slug = name.replace(' ', '-')
        category.updated_at = datetime.now()
        db.session.commit()
        return redirect(url_for('admin_bp.categories_view'))
    return render_template('admin/category_edit.html', category=category)


def authors_view():
    page, per_page, _ = get_page_args(page_parameter='page', per_page_parameter='per_page')
    authors = Authors.query.order_by(Authors.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    pagination = Pagination(page=page, per_page=per_page, total=authors.total)
    return render_template('admin/authors.html', authors=authors, page=page, per_page=per_page, pagination=pagination)


def author_add_view():
    if request.method == 'POST':
        name = request.form.get('name')
        original_name = request.form.get('original-name')
        bio = request.form.get('bio')
        if not name or not original_name or not bio:
            return render_template('admin/author_add.html')
        now = datetime.now()
        author = Authors(name=name, original_name=original_name, bio=bio, created_at=now, updated_at=now)
        db.session.add(author)
        db.session.commit()
        return redirect(url_for('admin_bp.authors_view'))
    return render_template('admin/author_add.html')


def author_edit_view():
    author = Authors.query.filter_by(id=request.args.get('id')).first_or_404()
    if request.method == 'POST':
        name = request.form.get('name')
        original_name = request.form.get('original-name')
        bio = request.form.get('bio')
        if not name or not original_name or not bio:
            return render_template('admin/author_edit.html', author=author)
        author.name = name
        author.original_name = original_name
        author.bio = bio
        author.updated_at = datetime.now()
        db.session.commit()
        return redirect(url_for('admin_bp.authors_view'))
    return render_template('admin/author_edit.html', author=author)
