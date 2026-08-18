from datetime import datetime
from secrets import token_urlsafe
from werkzeug.security import check_password_hash, generate_password_hash
from config import db
from models.User import Users


class AuthService:
    def find_by_email(self, email):
        return Users.query.filter(Users.email == email).first()

    def register(self, email, password, client_ip):
        if self.find_by_email(email):
            return None
        now = datetime.now()
        user = Users(email=email, password=generate_password_hash(password, method='SHA256'), session_token=token_urlsafe(32), created_at=now, creator_ip=client_ip, updated_at=now, updater_ip=client_ip)
        db.session.add(user)
        db.session.commit()
        return user

    def authenticate(self, email, password):
        user = self.find_by_email(email)
        if not user or not check_password_hash(user.password, password):
            return None
        user.session_token = token_urlsafe(32)
        db.session.commit()
        return user
