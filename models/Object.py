from config import db

class Objects(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    object_name = db.Column(db.String(255), nullable=False)
    bucket = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    creator_ip = db.Column(db.String(15), nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    updater_ip = db.Column(db.String(15), nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    deletor_ip = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        return self.object_name