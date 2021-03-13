import math
import os
import random
import uuid

from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_selfdoc import Autodoc
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer

from utils import Randomizer

# Init
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_BINDS'] = {
    'db': 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
}
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)
# Auto doc
auto = Autodoc(app)


class Dungeon(db.Model):
    id = Column('id', Integer, primary_key=True, default=uuid.uuid4)
    name = Column('name', String(20), unique=True)
    level = Column('level', Integer)
    experience = Column('experience', Integer)

    def __init__(self, id, name, level, experience):
        self.id = id
        self.name = name
        self.level = level
        self.experience = experience


# Dungeon Schema
class DungeonSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'level', 'experience')


# Init schema
dungeon_schema = DungeonSchema()
dungeons_schema = DungeonSchema(many=True)


@app.route('/', methods=['GET'])
def index():
    return 'index'


@app.route('/documentation')
def documentation():
    return auto.html(title='Dungeons Documentation')


# Create a Dungeon
@auto.doc(groups='private', set_location=False)
@app.route('/dungeon', methods=['POST'])
def add_dungeon():
    id = request.json['id']
    name = request.json['name']
    level = request.json['level']
    experience = request.json['experience']

    new_dungeon = Dungeon(id, name, level, experience)

    db.session.add(new_dungeon)
    db.session.commit()

    return dungeon_schema.jsonify(new_dungeon)


# Get All Dungeons
@auto.doc(groups='private', set_location=False)
@app.route('/dungeon', methods=['GET'])
def get_dungeons():
    all_dungeons = Dungeon.query.all()
    result = dungeons_schema.dump(all_dungeons)
    return jsonify(result)


# Get Single Dungeon
@auto.doc(groups='private', set_location=False)
@app.route('/dungeon/<id>', methods=['GET'])
def get_dungeon(id):
    dungeon = Dungeon.query.get(id)
    return dungeon_schema.jsonify(dungeon)


# Update a Dungeon
@auto.doc(groups='private', set_location=False)
@app.route('/dungeon/<id>', methods=['PUT'])
def update_dungeon(id):
    dungeon = Dungeon.query.get(id)

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
@auto.doc(groups='private', set_location=False)
@app.route('/dungeon/<id>', methods=['DELETE'])
def delete_dungeon(id):
    dungeon = Dungeon.query.get(id)
    db.session.delete(dungeon)
    db.session.commit()
    return dungeon_schema.jsonify(dungeon)


"""
DEBUG
"""


@app.route('/generate', methods=['GET', 'POST'])
@auto.doc(groups='private', set_location=False)
def generate_dungeon():
    rand_name = Randomizer.random_name(20)
    rand_level = random.randint(1, 100)

    id = random.randint(1, pow(2, 63))
    name = rand_name
    level = rand_level
    experience = random.randint(rand_level, int(rand_level * pow(rand_level, math.tau)))

    new_dungeon = Dungeon(id, name, level, experience)

    db.session.add(new_dungeon)
    db.session.commit()

    return dungeon_schema.jsonify(new_dungeon)


if __name__ == '__main__':
    db.create_all()
    app.run()
