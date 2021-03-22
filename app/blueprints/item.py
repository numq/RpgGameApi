from flask import request

from app.blueprints import bp_item
from app.extensions import db
from app.utilities.generators import AppGenerator, ItemGenerator
from database import models
from database.schemes import item_schema, items_schema


# Create Item
@bp_item.route('/inventory/<character_id>/<id>', methods=['POST'])
def create_item(character_id=None):
    item = models.Item(character_id=character_id)
    if db.session.query(models.Item).filter_by(id=item.id).count() < 1:
        db.session.add(item)
        db.session.commit()

    return item_schema.jsonify(item)


# Get Single Item
@bp_item.route('/inventory/<character_id>/<id>', methods=['GET'])
def get_item(character_id=None, id=None):
    item = models.Item.query.get(id)
    return item_schema.jsonify(item)


# Get Inventory
@bp_item.route('/inventory/<character_id>', methods=['GET'])
def get_inventory(character_id=None):
    items = models.Item.query.filter_by(character_id=character_id).all()
    return items_schema.jsonify(items)


# Update Item
@bp_item.route('/inventory/<character_id>/<id>', methods=['PUT'])
def update_item(character_id=None, id=None):
    item = models.Item.get(id).first()

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
    item = models.Item.query.get(id)
    db.delete(item)
    db.session.commit()
    return item_schema.jsonify(item)


# Generate Item Drop
@bp_item.route('/inventory/<character_id>/drop', methods=['POST'])
def generate_drop(character_id=None):
    dungeon_id = request.json['dungeon_id']
    dungeon = models.Dungeon.query.get(dungeon_id)

    name = AppGenerator().generate_name_by_pattern('RandomItem')

    level = ItemGenerator().generate_level_by_dungeon(dungeon.level)
    type = ItemGenerator().generate_type()
    rarity = ItemGenerator().generate_rarity()
    stats = ItemGenerator().generate_stats(level, rarity)
    cost = ItemGenerator().generate_cost(level, rarity)

    item = models.Item()

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
