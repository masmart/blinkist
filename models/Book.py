from config import db


class Ideas(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text(), nullable=False)
    sample_text = db.Column(db.Text(), nullable=True)
    order = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Idea %r>' % self.title


class Audios(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    idea_id = db.Column(db.Integer, db.ForeignKey('ideas.id'), nullable=False)
    idea = db.relationship("Ideas", backref=db.backref("audios", lazy=True))
    file = db.Column(db.String(2083), nullable=False)
    sample_file = db.Column(db.String(2083), nullable=True)
    order = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    
class Books(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    tagline = db.Column(db.String(255), nullable=False)
    tagline_html = db.Column(db.String(255), nullable=False)
    read_time = db.Column(db.Integer, nullable=False)
    ideas = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(120), nullable=False)
    has_audio = db.Column(db.Boolean, nullable=False)
    description = db.Column(db.Text, nullable=False)
    published_at = db.Column(db.DateTime, nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    total_rating = db.Column(db.Integer, nullable=True)
    who_should_read_1 = db.Column(db.String(255), nullable=True)
    who_should_read_2 = db.Column(db.String(255), nullable=True)
    who_should_read_3 = db.Column(db.String(255), nullable=True)
    best_quote = db.Column(db.String(255), nullable=True)
    cover_image = db.Column(db.String(2083), nullable=True)
    purchase_url = db.Column(db.String(255), nullable=True)
    slug = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    original_title = db.Column(db.String(255), nullable=False)
    idea_book = db.relationship('Ideas', backref='idea_book', lazy=True, foreign_keys=[Ideas.book_id])
    audio_book = db.relationship('Audios', backref='audio_book', lazy=True, foreign_keys=[Audios.book_id])
    # idea_book = db.relationship("IdeaBook", back_populates="books")
    # audio_book = db.relationship("AudioBook", back_populates="books")
    authors = db.relationship("Authors", secondary="book_authors", backref=db.backref("books", lazy=True))
    categories = db.relationship("Categories", secondary="book_categories", backref=db.backref(name="books", lazy=True))
    topics = db.relationship("Topics", secondary="book_topics")

    def __repr__(self):
        return '<Books %r>' % self.title


book_authors = db.Table('book_authors',
    db.Column('book_id', db.Integer, db.ForeignKey('books.id'), primary_key=True),
    db.Column('author_id', db.Integer, db.ForeignKey('authors.id'), primary_key=True)
)

book_categories = db.Table('book_categories',
    db.Column('book_id', db.Integer, db.ForeignKey('books.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
)

book_topics = db.Table('book_topics',
    db.Column('book_id', db.Integer, db.ForeignKey('books.id'), primary_key=True),
    db.Column('topic_id', db.Integer, db.ForeignKey('topics.id'), primary_key=True)
)
