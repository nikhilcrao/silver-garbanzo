import os

from flask import Flask, redirect, url_for
from flask_bootstrap import Bootstrap


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.instance_path, 'db.sqlite'),
        UPLOAD_FOLDER = os.path.join(app.instance_path, 'uploads'),
    )

    Bootstrap(app)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
        os.makedirs(os.path.join(app.instance_path, 'uploads'))
    except OSError:
        pass

    from . import database
    database.init_app(app)
    
    from . import auth
    auth.init_app(app)
    app.register_blueprint(auth.bp)

    from . import category
    app.register_blueprint(category.bp)

    from . import merchant
    app.register_blueprint(merchant.bp)

    from . import rule
    app.register_blueprint(rule.bp)
    
    @app.cli.command('reset-db')
    def reset_db():
        database.reset_db(app)

    @app.route('/')
    def index():
        return redirect(url_for('category.index'))

    return app