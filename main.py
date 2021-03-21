from flask_selfdoc import Selfdoc
from flask_sqlalchemy import SQLAlchemy

from app import create_app, register_blueprints
from config import ProductionConfig

# Init
app = create_app(ProductionConfig)
app.url_map.strict_slashes = False

# Init db
db = SQLAlchemy(app)

# Auto doc
auto = Selfdoc(app)

if __name__ == "__main__":
    db.init_app(app)
    register_blueprints(app)
    app.run()
