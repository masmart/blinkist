from datetime import datetime

from config import db


class TimestampMixin:
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class SoftDeleteMixin:
    deleted_at = db.Column(db.DateTime, nullable=True, index=True)

    @classmethod
    def active(cls):
        return cls.query.filter(cls.deleted_at.is_(None))

    def soft_delete(self):
        self.deleted_at = datetime.utcnow()


class AuditMixin:
    creator_ip = db.Column(db.String(15), nullable=False)
    updater_ip = db.Column(db.String(15), nullable=False)
    deletor_ip = db.Column(db.String(15), nullable=True)
