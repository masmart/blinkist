from datetime import datetime
from config import db
from models.User import Bookmarks


class BookmarkService:
    def find(self, user_id, book_id):
        return Bookmarks.query.filter_by(user_id=user_id, book_id=book_id, deleted_at=None).first()

    def is_bookmarked(self, user_id, book_id):
        return self.find(user_id, book_id) is not None

    def add(self, user_id, book_id, client_ip):
        existing = self.find(user_id, book_id)
        if existing:
            return existing
        now = datetime.now()
        bookmark = Bookmarks(user_id=user_id, book_id=book_id, created_at=now, creator_ip=client_ip, updated_at=now, updater_ip=client_ip)
        db.session.add(bookmark)
        db.session.commit()
        return bookmark

    def remove(self, user_id, book_id, client_ip):
        bookmark = self.find(user_id, book_id)
        if bookmark is None:
            return False
        bookmark.deleted_at = datetime.now()
        bookmark.deletor_ip = client_ip
        db.session.commit()
        return True
