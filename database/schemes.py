from app.extensions import ma


# User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'password_hash', 'created_on', 'updated_on')


# Character Schema
class CharacterSchema(ma.Schema):
    class Meta:
        fields = (
            'id', 'user_id', 'name', 'level', 'stats', 'hp', 'energy', 'experience', 'gold', 'inventory',
            'created_on',
            'updated_on')


# Item Schema
class ItemSchema(ma.Schema):
    class Meta:
        fields = (
            'id', 'character_id', 'name', 'description', 'dungeon_id', 'level', 'type', 'stats', 'cost', 'equipped',
            'created_on', 'updated_on')


# Ability Schema
class AbilitySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'effect', 'created_on', 'updated_on')


# Dungeon Schema
class DungeonSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'level', 'experience', 'duration', 'created_on', 'updated_on')


# Init user schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Init character schema
character_schema = CharacterSchema()
characters_schema = CharacterSchema(many=True)

# Init item schema
item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

# Init ability schema
ability_schema = AbilitySchema()
abilities_schema = AbilitySchema(many=True)

# Init dungeon schema
dungeon_schema = DungeonSchema()
dungeons_schema = DungeonSchema(many=True)
