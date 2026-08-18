from config import db
from models.mixins import AuditMixin, SoftDeleteMixin, TimestampMixin

class Objects(TimestampMixin, SoftDeleteMixin, AuditMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    object_name = db.Column(db.String(255), nullable=False, unique=True, index=True)
    bucket = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return self.object_name


StoredObject = Objects
