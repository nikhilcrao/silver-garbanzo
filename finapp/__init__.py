import os

from flask import Flask, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect


bootstrap = Bootstrap5()
csrf = CSRFProtect()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.instance_path, 'db.sqlite'),
        UPLOAD_FOLDER = os.path.join(app.instance_path, 'uploads'),
    )

    bootstrap.init_app(app)
    csrf.init_app(app)


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

    from . import record
    app.register_blueprint(record.bp)

    @app.cli.command('reset-db')
    def reset_db():
        database.reset_db(app)

    @app.cli.command('init-category')
    def init_category():
        database.init_category(app)

    @app.cli.command('init-records')
    def init_records():
        database.init_records(app)
    
    @app.route('/')
    def index():
        return redirect(url_for('record.index'))

    return app