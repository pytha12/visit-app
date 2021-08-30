"""
This is the User module and supports all the REST actions for the
user data
"""

from flask import make_response, abort
from config import db
from models import User, UserSchema, Visit


def read_all():
    """
    This function responds to a request for /api/users
    with the complete lists of users

    :return:        json string of list of user
    """
    # Create the list of users from our data
    user = User.query.order_by(User.lname).all()

    # Serialize the data for the response
    user_schema = UserSchema(many=True)
    data = user_schema.dump(user).data
    return data


def read_one(user_id):
    """
    This function responds to a request for /api/people/{user_id}
    with one matching user from people

    :param user_id:   Id of user to find
    :return:            user matching id
    """
    # Build the initial query
    user = (
        User.query.filter(User.user_id == user_id)
        .outerjoin(Visit)
        .one_or_none()
    )

    # Did we find a user?
    if user is not None:

        # Serialize the data for the response
        user_schema = UserSchema()
        data = user_schema.dump(user).data
        return data

    # Otherwise, nope, didn't find that user
    else:
        abort(404, f"User not found for Id: {user_id}")


def create(user):
    """
    This function creates a new user 
    based on the passed in user data

    :param user:  user to create in people structure
    :return:        201 on success, 409 on user exists
    """
    fname = user.get("fname")
    lname = user.get("lname")

    existing_user = (
        User.query.filter(User.fname == fname)
        .filter(User.lname == lname)
        .one_or_none()
    )

    # Does the user already exist or not?
    if existing_user is None:

        # Create a user instance using the schema and the passed in user
        schema = UserSchema()
        new_user = schema.load(user, session=db.session).data

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        # Serialize and return the newly created user in the response
        data = schema.dump(new_user).data

        return data, 201

    # Otherwise, user exists already
    else:
        abort(409, f"User {fname} {lname} exists already")


def update(user_id, user):
    """
    This function updates an existing user in the people structure

    :param user_id:   Id of the user to update in the people structure
    :param user:      user to update
    :return:            updated user structure
    """
    # Get the user requested from the db into session
    update_user = User.query.filter(
        User.user_id == user_id
    ).one_or_none()

    # Did we find an existing user?
    if update_user is not None:

        # turn the passed in user into a db object
        schema = UserSchema()
        update = schema.load(user, session=db.session).data

        # Set the id to the user we want to update
        update.user_id = update_user.user_id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated user in the response
        data = schema.dump(update_user).data

        return data, 200

    # Otherwise, nope, didn't find that user
    else:
        abort(404, f"User not found for Id: {user_id}")


def delete(user_id):
    """
    This function deletes a user from the people structure

    :param user_id:   Id of the user to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the user requested
    user = User.query.filter(User.user_id == user_id).one_or_none()

    # Did we find a user?
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        return make_response(f"User {user_id} deleted", 200)

    # Otherwise, nope, didn't find that user
    else:
        abort(404, f"User not found for Id: {user_id}")
