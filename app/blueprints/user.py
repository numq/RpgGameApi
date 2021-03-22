from flask import request

from app.blueprints import bp_user
from app.extensions import db
from app.utilities import exceptions
from database import models
from database.schemes import user_schema, users_schema


# Create User
@bp_user.route('/users/create', methods=['POST'])
def create_user():
    new_user = models.User()
    new_user.name = request.json['name']
    new_user.email = request.json['email']
    new_user.password_hash = new_user.set_password(request.json['password'])

    if db.session.query(models.User).filter_by(id=new_user.id, email=new_user.email).count() < 1:
        db.session.add(new_user)
        db.session.commit()
        return user_schema.jsonify(new_user)
    else:
        return exceptions.DbEntryExists[0], exceptions.DbEntryExists[1]


# Get Single User
@bp_user.route('/users/<id>', methods=['GET'])
def get_user(id=None):
    user = models.User.query.get(id)
    return user_schema.jsonify(user)


# Get All Users
@bp_user.route('/users', methods=['GET'])
def get_users():
    all_users = models.User.query.all()
    result = users_schema.jsonify(all_users)
    return result


# Update User
@bp_user.route('/users/<id>', methods=['PUT'])
def update_user(id=None):
    user = models.User.query.get(id)
    user.id = request.json['id']
    user.name = request.json['name']
    user.email = request.json['email']
    user.password_hash = user.set_password(request.json['password'])
    db.session.commit()
    return user_schema.jsonify(user)


# Delete User
@bp_user.route('/users/<id>', methods=['DELETE'])
def delete_user(id=None):
    user = models.User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)
