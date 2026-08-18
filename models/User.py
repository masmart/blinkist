from flask_login import UserMixin
from config import db, login_manager


class Users(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=True)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(140), nullable=False)
    session_token = db.Column(db.String(100), unique=True)
    bookmarks = db.relationship("Bookmarks", backref="user", lazy=True)
    created_at = db.Column(db.DateTime, nullable=False)
    creator_ip = db.Column(db.String(15), nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    updater_ip = db.Column(db.String(15), nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    deletor_ip = db.Column(db.String(15), nullable=True)

    followed_topics = db.relationship("Topics", secondary="user_topics")

    def __repr__(self):
        if self.full_name:
            return self.full_name
        else:
            return self.email

    def get_id(self):
        return str(self.session_token)

@login_manager.user_loader
def user_loader(session_token):
    return Users.query.filter_by(session_token=session_token).first()

class Bookmarks(db.Model):

    __table_args__ = (
        db.Index(
            'uq_active_bookmark_user_book',
            'user_id',
            'book_id',
            unique=True,
            postgresql_where=db.text('deleted_at IS NULL'),
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)
    creator_ip = db.Column(db.String(15), nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    updater_ip = db.Column(db.String(15), nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    deletor_ip = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        if self.book_id and self.deleted_at is None:
            return str(self.book_id)
        else:
            return "Deleted"
