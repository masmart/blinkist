from flask import Flask, render_template, url_for, send_from_directory, request
from flask_migrate import Migrate
from config import db, login_manager, admin

from controllers import AdminController
from routes.author_bp import author_bp
from routes.book_bp import book_bp
from routes.collection_bp import collection_bp
from routes.category_bp import category_bp
from routes.topic_bp import topic_bp
from routes.user_bp import user_bp
from routes.dashboard_bp import dashboard_bp
from routes.api_bp import api_bp

import os

def create_app():
    app = Flask('__name__')
    
app.config.from_pyfile('config.py')
db.init_app(app)
login_manager.init_app(app)
with app.app_context():
    login_manager.login_view = '/user/login'
migrate = Migrate(app, db)

admin.init_app(app)
AdminController.init()

from models import Author, Book, Category, Topic, User

app.register_blueprint(author_bp, url_prefix='/author')
app.register_blueprint(book_bp, url_prefix='/book')
app.register_blueprint(collection_bp, url_prefix='/collection')
app.register_blueprint(category_bp, url_prefix='/category')
app.register_blueprint(topic_bp, url_prefix='/topic')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def main():

    return render_template('views/main/main.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'images/favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == ('__main__'):
    app.run()