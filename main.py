import math
import os
import random
import uuid
from datetime import datetime

from flask import Flask, request, jsonify, json
from flask_marshmallow import Marshmallow
from flask_selfdoc import Autodoc
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, JSON, DateTime

from utils import Randomizer, AppConstants, Generator, AppExceptions

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


# User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('user_token', 'registration_datetime')


# Character Schema
class CharacterSchema(ma.Schema):
    class Meta:
        fields = ('user_token', 'id', 'name', 'level', 'stats')


# Dungeon Schema
class DungeonSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'level', 'experience')


class User(db.Model):
    __tablename__ = 'users'

    user_token = Column('user_token', Integer, primary_key=True)
    registration_datetime = Column('registration_datetime', DateTime)

    def __init__(self, user_token, registration_datetime):
        self.user_token = user_token
        self.registration_datetime = registration_datetime

    def __repr__(self) -> str:
        return f"User('{self.user_token}', '{self.registration_datetime}')"


class Character(db.Model):
    __tablename__ = 'characters'

    user_token = Column('user_token', Integer, nullable=False)
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(120), nullable=False)
    level = Column('level', Integer, nullable=False)
    stats = Column('stats', JSON, nullable=False)

    def __init__(self, user_token, id, name, level, stats):
        self.user_token = user_token
        self.id = id
        self.name = name
        self.level = level
        self.stats = stats

    def __repr__(self) -> str:
        return f"Character('{self.id}', '{self.name}', '{self.level}', '{self.stats}')"


class Dungeon(db.Model):
    __tablename__ = 'dungeons'

    id = Column('id', Integer, primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column('name', String(20), nullable=False)
    level = Column('level', Integer, nullable=False)
    experience = Column('experience', Integer, nullable=False)

    def __init__(self, id, name, level, experience):
        self.id = id
        self.name = name
        self.level = level
        self.experience = experience

    def __repr__(self) -> str:
        return f"Dungeon('{self.id}', '{self.name}', '{self.level}', '{self.experience}')"


# Init character schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Init character schema
character_schema = CharacterSchema()
characters_schema = CharacterSchema(many=True)

# Init dungeon schema
dungeon_schema = DungeonSchema()
dungeons_schema = DungeonSchema(many=True)


@app.route('/', methods=['GET'])
def index():
    return 'index'


@app.route('/documentation')
def documentation():
    return auto.html(title='Documentation')


"""
    User
"""


@auto.doc(groups='private', set_location=False)
@app.route('/users/create_user', methods=['POST'])
def create_user():
    user_token = request.json['user_token']

    if db.session.query(User).filter_by(user_token=user_token).count() < 1:
        new_user = User(user_token=user_token, registration_datetime=datetime.utcnow())
        db.session.add(new_user)
        db.session.commit()

        return user_schema.jsonify(new_user)
    else:
        return AppExceptions.DbEntryExists[0], AppExceptions.DbEntryExists[1]


# Get Single User
@auto.doc(groups='private', set_location=False)
@app.route('/users/<user_token>', methods=['GET'])
def get_user(user_token):
    user = User.query.get(user_token)
    return user_schema.jsonify(user)


# Get All Users
@auto.doc(groups='private', set_location=False)
@app.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)


# Delete User
@auto.doc(groups='private', set_location=False)
@app.route('/users/<user_token>', methods=['DELETE'])
def delete_user(user_token):
    user = User.query.get(user_token)
    db.session.delete(user)
    db.session.commit()
    return character_schema.jsonify(user)


"""
    Character
"""


# Create a Character
@auto.doc(groups='private', set_location=False)
@app.route('/users/<user_token>/create_character', methods=['POST'])
def create_character(user_token=None):
    id = request.json['id']
    name = request.json['name']
    level = request.json['level']
    stats = json.dumps(Generator().generate_stats(AppConstants.MAX_NEW_CHAR_STATS), indent=4)

    if db.session.query(Character).filter_by(user_token=user_token, id=id).count() < 1:
        new_character = Character(user_token, id, name, level, stats)
        db.session.add(new_character)
        db.session.commit()

        return character_schema.jsonify(new_character)
    else:
        return AppExceptions.DbEntryExists[0], AppExceptions.DbEntryExists[1]


# Get All Characters
@auto.doc(groups='private', set_location=False)
@app.route('/users/<user_token>/characters', methods=['GET'])
def get_characters(user_token=None):
    all_characters = Character.query.filter_by(user_token=user_token).all()
    result = characters_schema.dump(all_characters)
    return jsonify(result)


# Get Single Character
@auto.doc(groups='private', set_location=False)
@app.route('/users/<user_token>/<id>', methods=['GET'])
def get_character(user_token=None, id=None):
    character = Character.query.filter_by(user_token=user_token, id=id).get(id)
    return character_schema.jsonify(character)


# Update a Character
@auto.doc(groups='private', set_location=False)
@app.route('/users/<user_token>/<id>', methods=['PUT'])
def update_character(user_token=None, id=None):
    character = Character.query.filter_by(user_token=user_token, id=id).get(id)

    user_token = request.json['user_token']
    id = request.json['id']
    name = request.json['name']
    level = request.json['level']
    stats = request.json['stats']

    character.user_token = user_token
    character.id = id
    character.name = name
    character.level = level
    character.stats = stats

    db.session.commit()

    return character_schema.jsonify(character)


# Delete Character
@auto.doc(groups='private', set_location=False)
@app.route('/users/<user_token>/<id>', methods=['DELETE'])
def delete_character(user_token=None, id=None):
    character = Character.query.filter_by(user_token=user_token, id=id).get(id)
    db.session.delete(character)
    db.session.commit()
    return character_schema.jsonify(character)


"""
    DUNGEON
"""


# Create a Dungeon
@auto.doc(groups='private', set_location=False)
@app.route('/dungeon', methods=['POST'])
def add_dungeon():
    id = request.json['id']
    name = request.json['name']
    level = request.json['level']
    experience = request.json['experience']

    if db.session.query(Dungeon).filter_by(id=id).count() < 1:
        new_dungeon = Dungeon(id, name, level, experience)
        db.session.add(new_dungeon)
        db.session.commit()

        return dungeon_schema.jsonify(new_dungeon)
    else:
        return AppExceptions.DbEntryExists[0], AppExceptions.DbEntryExists[1]


# Get All Dungeons
@auto.doc(groups='private', set_location=False)
@app.route('/dungeons', methods=['GET'])
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


@app.route('/generate', methods=['POST'])
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
    app.run(debug=True)
