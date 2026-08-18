from flask import Flask, render_template, send_from_directory
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config import db, get_config, login_manager

import os

csrf = CSRFProtect()
migrate = Migrate()


def create_app(config_name=None, config_overrides=None):
    """Create and configure a Blinkist application instance."""
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))
    if config_overrides:
        app.config.update(config_overrides)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    login_manager.login_view = '/user/login'

    register_blueprints(app)
    register_routes(app)
    return app


def register_blueprints(app):
    from routes.admin_bp import admin_bp
    from routes.author_bp import author_bp
    from routes.book_bp import book_bp
    from routes.collection_bp import collection_bp
    from routes.category_bp import category_bp
    from routes.topic_bp import topic_bp
    from routes.user_bp import user_bp
    from routes.dashboard_bp import dashboard_bp
    from routes.api_bp import api_bp
    from routes.upload_bp import upload_bp

    blueprints = (
        (admin_bp, '/admin'),
        (author_bp, '/author'),
        (book_bp, '/book'),
        (collection_bp, '/collection'),
        (category_bp, '/category'),
        (topic_bp, '/topic'),
        (user_bp, '/user'),
        (dashboard_bp, '/dashboard'),
        (api_bp, '/api'),
        (upload_bp, '/upload'),
    )
    for blueprint, prefix in blueprints:
        app.register_blueprint(blueprint, url_prefix=prefix)


def register_routes(app):
    from models.Book import Books
    from models.Category import Categories

    @app.route('/')
    def main():
        top_links = Books.query.order_by(Books.id.desc()).limit(6).all()
        categories = Categories.query.all()
        latest = Books.query.order_by(Books.id.asc()).limit(20).all()
        top_four_for_today = Books.query.order_by(Books.published_at.asc()).limit(4).all()
        return render_template(
            'views/main/main.html',
            top_links=top_links,
            categories=categories,
            latest=latest,
            top_four_for_today=top_four_for_today,
        )

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(
            os.path.join(app.root_path, 'static'),
            'images/favicon.ico',
            mimetype='image/vnd.microsoft.icon',
        )


if __name__ == '__main__':
    app = create_app()
    app.run()
