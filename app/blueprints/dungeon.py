# Create a Dungeon
from datetime import timedelta, datetime

from flask import request

from app.blueprints import bp_dungeon
from app.extensions import db
from app.utilities import exceptions
from app.utilities.generators import DungeonGenerator, AppGenerator
from database import models
from database.schemes import dungeons_schema, dungeon_schema


@bp_dungeon.route('/dungeons/create', methods=['POST'])
def create_dungeon():
    name = request.json['name']
    level = request.json['level']
    experience = request.json['experience']

    new_dungeon = models.Dungeon(name=name, level=level, experience=experience)

    if db.session.query(models.Dungeon).filter_by(id=new_dungeon.id).count() < 1:
        db.session.add(new_dungeon)
        db.session.commit()

        duration = datetime.utcnow() + timedelta(minutes=DungeonGenerator().generate_duration())
        new_dungeon.duration = duration

        return dungeon_schema.jsonify(new_dungeon)
    else:
        return exceptions.DbEntryExists[0], exceptions.DbEntryExists[1]


# Get Single Dungeon
@bp_dungeon.route('/dungeons/<id>', methods=['GET'])
def get_dungeon(id=None):
    dungeon = models.Dungeon.query.get(id)
    return dungeon_schema.jsonify(dungeon)


# Get All Dungeons
@bp_dungeon.route('/dungeons', methods=['GET'])
def get_dungeons():
    all_dungeons = models.Dungeon.query.all()
    return dungeons_schema.jsonify(all_dungeons)


# Update a Dungeon
@bp_dungeon.route('/dungeons/<id>', methods=['PUT'])
def update_dungeon(id=None):
    dungeon = models.Dungeon.query.get(id)

    id = request.json['id']
    name = request.json['name']
    level = request.json['level']
    experience = request.json['experience']

    dungeon.id = id
    dungeon.name = name
    dungeon.level = level
    dungeon.experience = experience

    db.session.commit()

    return dungeon_schema.jsonify(dungeon)


# Delete Dungeon
@bp_dungeon.route('/dungeons/<id>', methods=['DELETE'])
def delete_dungeon(id=None):
    dungeon = models.Dungeon.query.get(id)
    db.session.delete(dungeon)
    db.session.commit()
    return dungeon_schema.jsonify(dungeon)


# Generate Dungeon
@bp_dungeon.route('/dungeons/generate', methods=['POST'])
def generate_dungeon():
    rand_name = AppGenerator().generate_name_by_pattern('Dungeon')
    rand_level = DungeonGenerator().generate_level()

    name = rand_name
    level = rand_level
    experience = DungeonGenerator().generate_experience(level)
    duration = datetime.utcnow() + timedelta(minutes=DungeonGenerator().generate_duration())

    new_dungeon = models.Dungeon(name=name, level=level, experience=experience, duration=duration)

    db.session.add(new_dungeon)
    db.session.commit()

    return dungeon_schema.jsonify(new_dungeon)
