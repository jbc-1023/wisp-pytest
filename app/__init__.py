import os

from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='hellowisp',
        DATABASE=os.path.join(app.instance_path, 'tic_tac_toe.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from app.routes import auth, game, ping
    app.register_blueprint(ping.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(game.bp)

    return app
