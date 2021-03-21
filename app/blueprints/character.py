from flask import request, jsonify, json, Blueprint

from app.utilities import constants, exceptions
from app.utilities.generators import CharacterGenerator
from database.models import Character, User
from database.schemes import character_schema, characters_schema
from main import db

bp_character = Blueprint('character', __name__)


# Create a Character
@bp_character.route('/characters/create', methods=['POST'])
def create_character():
    generated_stats = CharacterGenerator().generate_stats(constants.MAX_NEW_CHAR_STATS)

    user_id = request.json['user_id']
    name = CharacterGenerator().generate_classname(stats=generated_stats)
    level = constants.NEW_CHAR_LEVEL
    stats = json.dumps(generated_stats)
    hp = constants.DEFAULT_HP
    energy = constants.DEFAULT_ENERGY
    experience = constants.NEW_CHAR_EXPERIENCE
    gold = constants.NEW_CHAR_GOLD
    inventory = json.dumps(list())

    new_character = Character(user_id=user_id, name=name, level=level, stats=stats, hp=hp, energy=energy,
                              experience=experience, gold=gold, inventory=inventory)
    if db.session.query(User).filter_by(id=new_character.user_id).count() > 0 and db.session.query(Character).filter_by(
            user_id=new_character.user_id, id=new_character.id).count() < 1:
        db.session.add(new_character)
        db.session.commit()
        return character_schema.jsonify(new_character)
    else:
        return exceptions.DbEntryExists[0], exceptions.DbEntryExists[1]


# Get All Characters
@bp_character.route('/characters', methods=['GET'])
def get_all_characters():
    all_characters = Character.query.all()
    result = characters_schema.dump(all_characters)
    return jsonify(result)


# Get Characters
@bp_character.route('/users/<user_id>/characters', methods=['GET'])
def get_characters(user_id=None):
    characters = db.session.query(Character).filter_by(user_id=user_id).all()
    result = characters_schema.dump(characters)
    return jsonify(result)


# Get Single Character
@bp_character.route('/characters/<id>', methods=['GET'])
def get_character(id=None):
    character = Character.query.get(id)
    return character_schema.jsonify(character)


# Update a Character
@bp_character.route('/characters/<id>', methods=['PUT'])
def update_character(id=None):
    character = Character.query.get(id)

    name = request.json['name']
    level = request.json['level']
    stats = request.json['stats']
    hp = request.json['hp']
    energy = request.json['energy']
    experience = request.json['experience']
    gold = request.json['gold']
    inventory = request.json['inventory']

    character.name = name
    character.level = level
    character.stats = stats
    character.hp = hp
    character.energy = energy
    character.experience = experience
    character.gold = gold
    character.inventory = inventory

    db.session.commit()

    return character_schema.jsonify(character)


# Update Character Level
@bp_character.route('/characters/<id>/level', methods=['PUT'])
def update_character_level(id=None):
    character = Character.query.get(id)

    level = request.json['level']

    character.level = level

    db.session.commit()

    return character_schema.jsonify(character)


# Delete Character
@bp_character.route('/characters/<id>', methods=['DELETE'])
def delete_character(id=None):
    character = Character.query.get(id)
    db.session.delete(character)
    db.session.commit()
    return character_schema.jsonify(character)
