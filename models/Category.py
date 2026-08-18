from config import db
from models.mixins import SoftDeleteMixin, TimestampMixin


class Categories(TimestampMixin, SoftDeleteMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False, unique=True, index=True)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.Text, nullable=True)
    titles = db.Column(db.Integer, nullable=True)
    original_name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return self.name


Category = Categories
