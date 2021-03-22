from flask import Flask

from config import TestConfig


def create_app(config=TestConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    app.url_map.strict_slashes = False
    register_extensions(app)
    register_blueprints(app)

    from app.extensions import db
    db.create_all(app=app)
    return app


def register_extensions(app):
    from app.extensions import db, ma, auto
    db.init_app(app)
    ma.init_app(app)
    auto.init_app(app)
    return None


def register_blueprints(app):
    from app.blueprints.dev import bp_dev
    from app.blueprints.user import bp_user
    from app.blueprints.character import bp_character
    from app.blueprints.item import bp_item
    from app.blueprints.dungeon import bp_dungeon

    # Blueprints
    app.register_blueprint(bp_dev)
    app.register_blueprint(bp_user)
    app.register_blueprint(bp_character)
    app.register_blueprint(bp_item)
    app.register_blueprint(bp_dungeon)
    return None
