from config import db
from models.mixins import SoftDeleteMixin, TimestampMixin


class Collections(TimestampMixin, SoftDeleteMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    curator_id = db.Column(db.Integer, db.ForeignKey('curators.id'), nullable=False)
    curators = db.relationship("Curators", backref=db.backref("collections", lazy=True))
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False, unique=True, index=True)
    tagline = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    cover_image = db.Column(db.String(255), nullable=False)
    original_name = db.Column(db.String(255), nullable=False)

    books = db.relationship("Books", secondary="collection_books", backref=db.backref("collections", lazy=True))
    categories = db.relationship("Categories", secondary="collection_categories", backref=db.backref("collections", lazy=True))

    def __repr__(self):
        return self.name


class Curators(TimestampMixin, SoftDeleteMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    users = db.relationship("Users", backref=db.backref("curators", lazy=True))
    name = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return self.name


collection_books = db.Table('collection_books',
    db.Column('collection_id', db.Integer, db.ForeignKey('collections.id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('books.id'), primary_key=True)
)

collection_categories = db.Table('collection_categories',
    db.Column('collection_id', db.Integer, db.ForeignKey('collections.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
)


Collection = Collections
Curator = Curators
