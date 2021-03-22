from flask import Flask


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    return app


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
