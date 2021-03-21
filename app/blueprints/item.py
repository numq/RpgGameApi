from flask import request, Blueprint

from app.utilities.generators import AppGenerator, ItemGenerator
from database.models import Item, Dungeon, db
from database.schemes import item_schema, items_schema

bp_item = Blueprint('item', __name__)


# Create Item
@bp_item.route('/inventory/<character_id>/<id>', methods=['POST'])
def create_item(character_id=None):
    item = Item(character_id=character_id)
    if db.session.query(Item).filter_by(id=item.id).count() < 1:
        db.session.add(item)
        db.session.commit()

    return item_schema.jsonify(item)


# Get Single Item
@bp_item.route('/inventory/<character_id>/<id>', methods=['GET'])
def get_item(character_id=None, id=None):
    item = Item.query.get(id)
    return item_schema.jsonify(item)


# Get Inventory
@bp_item.route('/inventory/<character_id>', methods=['GET'])
def get_inventory(character_id=None):
    items = Item.query.filter_by(character_id=character_id).all()
    return items_schema.jsonify(items)


# Update Item
@bp_item.route('/inventory/<character_id>/<id>', methods=['PUT'])
def update_item(character_id=None, id=None):
    item = Item.get(id).first()

    name = request.json['name']
    description = request.json['description']
    level = request.json['level']
    type = request.json['type']
    stats = request.json['stats']
    cost = request.json['cost']
    equipped = request.json['equipped']

    item.character_id = character_id
    item.name = name
    item.description = description
    item.level = level
    item.type = type
    item.stats = stats
    item.cost = cost
    item.equipped = equipped

    db.session.commit()

    return item_schema.jsonify(item)


# Delete Item
@bp_item.route('/inventory/<character_id>/<id>', methods=['DELETE'])
def delete_item(id=None):
    item = Item.query.get(id)
    db.delete(item)
    db.session.commit()
    return item_schema.jsonify(item)


# Generate Item Drop
@bp_item.route('/inventory/<character_id>/drop', methods=['POST'])
def generate_drop(character_id=None):
    dungeon_id = request.json['dungeon_id']
    dungeon = Dungeon.query.get(dungeon_id)

    name = AppGenerator().generate_name_by_pattern('RandomItem')

    level = ItemGenerator().generate_level_by_dungeon(dungeon.level)
    type = ItemGenerator().generate_type()
    rarity = ItemGenerator().generate_rarity()
    stats = ItemGenerator().generate_stats(level, rarity)
    cost = ItemGenerator().generate_cost(level, rarity)

    item = Item()

    item.character_id = character_id
    item.name = name
    item.dungeon_id = dungeon_id
    item.level = level
    item.type = type
    item.stats = stats
    item.cost = cost
    item.equipped = False

    db.session.add(item)
    db.session.commit()

    return item_schema.jsonify(item)
