from sqlalchemy import asc
from models.Book import Books, Ideas
from models.Category import Categories


class BookService:
    def get_by_slug(self, slug):
        return Books.query.filter_by(slug=slug).first()

    def get_reader_content(self, slug, idea_order):
        book = self.get_by_slug(slug)
        if book is None:
            return None, [], None
        ideas = Ideas.query.filter_by(book_id=book.id).order_by(asc(Ideas.order)).all()
        selected = Ideas.query.filter_by(book_id=book.id, order=idea_order).one_or_none()
        return book, ideas, selected

    def similar(self, category_id, limit=10):
        if category_id is None:
            return []
        return Books.query.join(Books.categories).filter(Categories.id == category_id).order_by(Books.rating.asc()).limit(limit).all()

    def trending(self, category_id, limit=10):
        if category_id is None:
            return []
        return Books.query.join(Books.categories).filter(Categories.id == category_id).order_by(Books.total_rating.asc()).limit(limit).all()
