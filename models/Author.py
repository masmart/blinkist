from config import db
from models.mixins import SoftDeleteMixin, TimestampMixin

class Authors(TimestampMixin, SoftDeleteMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    original_name = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return self.name


Author = Authors
