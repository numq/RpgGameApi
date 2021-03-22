from flask import Blueprint

bp_dev = Blueprint('dev', __name__)

bp_user = Blueprint('user', __name__)
bp_character = Blueprint('character', __name__)
bp_dungeon = Blueprint('dungeon', __name__)
bp_item = Blueprint('item', __name__)
