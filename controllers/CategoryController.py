
from flask import render_template, redirect, url_for, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, asc

import sys

from models.Category import Categories
from models.Book import Books, book_categories
from models.Collection import Collections


db = SQLAlchemy()

def category_list_view():

    categories = Categories.query.order_by(asc(Categories.name)).all()

    return render_template('views/category/categories.html', items=categories)

def category_view(category_slug):

    root_dir = url_for('category_bp.category_list_view')
    category = Categories.query.filter_by(slug=category_slug).first()
    popular = Books.query.join(book_categories).join(Categories).filter(Categories.slug == category_slug).order_by(desc(Books.rating)).limit(8).all()
    classics = Books.query.join(book_categories).join(Categories).filter(Categories.slug == category_slug).order_by(desc(Books.total_rating)).limit(20).all()
    collections = Collections.query.join(Collections.categories).filter(Categories.slug == category_slug).order_by(Collections.created_at.asc()).limit(10).all()

    return render_template('views/category/category.html', category=category, popular=popular, classics=classics, root_dir=root_dir, collections=collections)

