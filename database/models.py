from sqlalchemy import Column, Integer, Text, func, String, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.utilities import constants
from database.enums import ItemType, ItemRarity
from main import app


class Base(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_on = Column(Text, default=func.now(), nullable=False)
    updated_on = Column(Text, default=func.now(), onupdate=func.now(), nullable=False)


class BaseNoId(db.Model):
    __abstract__ = True

    created_on = Column(Text, default=func.now(), nullable=False)
    updated_on = Column(Text, default=func.now(), onupdate=func.now(), nullable=False)


class User(Base):
    __tablename__ = 'users'

    name = Column(String(20), nullable=True)
    email = Column(String(120), unique=True)
    password_hash = Column(String(128))

    characters = relationship('Character', backref="user", lazy='dynamic')

    def __repr__(self) -> str:
        return f"User({self.id}, {self.name}, {self.email}, {self.created_on})"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Character(Base):
    __tablename__ = 'characters'

    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String(20))
    level = Column(Integer, default=1)
    stats = Column(JSON)
    hp = Column(Integer, default=constants.DEFAULT_HP)
    energy = Column(Integer, default=constants.DEFAULT_ENERGY)
    experience = Column(Integer, default=0)
    gold = Column(Integer, default=0)
    inventory = Column(JSON)

    items = relationship('Item', backref=backref("character", uselist=False))

    def __repr__(self) -> str:
        return f"Character({self.id}, {self.user_id}, {self.name}, {self.level}, {self.stats}, {self.experience}, {self.gold}, " \
               f"{self.inventory}, {self.created_on})"


class Item(Base):
    __tablename__ = 'items'

    character_id = Column(Integer, ForeignKey('characters.id'))

    name = Column(String(20))
    description = Column(String(120), nullable=True)
    dungeon_id = Column(Integer)
    level = Column(Integer)
    rarity = Column(db.Enum(ItemRarity))
    type = Column(db.Enum(ItemType))
    stats = Column(JSON)
    cost = Column(Integer)
    equipped = Column(Boolean)

    def __repr__(self) -> str:
        return f"Item({self.id}, {self.name}, {self.description}, {self.dungeon_id}, {self.level}, {self.rarity}, {self.type}, {self.stats}, {self.cost}, {self.equipped}, {self.created_on})"


class Ability(Base):
    __tablename__ = 'abilities'

    name = Column(String(20))
    description = Column(String, nullable=True)
    effect = Column(db.Enum, nullable=True)

    def __repr__(self) -> str:
        return f"Ability({self.id}, {self.name}, {self.description}, {self.effect}, {self.created_on})"


class Dungeon(Base):
    __tablename__ = 'dungeons'

    name = Column(String(20))
    level = Column(Integer)
    experience = Column(Integer)
    duration = Column(Text)

    def __repr__(self) -> str:
        return f"Dungeon({self.id}, {self.name}, {self.level}, {self.experience}, {self.duration}, {self.created_on})"


db.create_all(app=app, bind=['db', 'test'])
