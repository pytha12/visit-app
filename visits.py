"""
User Service Module: This module supports all the REST actions for the
user data
"""

from flask import make_response, abort
from config import db
from models import User, Visit, VisitSchema
from datetime import datetime, timezone


def read_all(page=1, per_page=10):
    """
    This function responds to a request for /api/user/visits
    with the complete list of visits, sorted by visit timestamp

    :return:                json list of all visits for all user
    """

    # Query the database for all the visits
    visits = Visit.query.order_by(db.desc(Visit.start_date)).paginate(page=page, per_page=per_page)

    # Serialize the list of visits from our data
    visit_schema = VisitSchema(many=True, exclude=["user.visits", "instructions", "visitor", "timestamp", "user.timestamp"])
    data = visit_schema.dump(visits.items).data
    return data


def read_one(user_id, visit_id):
    """
    This function responds to a request for
    /api/user/{user_id}/visits/{visit_id}
    with one matching visit for the associated user

    :param user_id:       Id of user the visit is related to
    :param visit_id:         Id of the visit
    :return:                json string of visit contents
    """
    # Query the database for the visit
    visit = (
        Visit.query.join(User, User.user_id == Visit.user_id)
        .filter(User.user_id == user_id)
        .filter(Visit.visit_id == visit_id)
        .one_or_none()
    )

    # Was a visit found?
    if visit is not None:
        visit_schema = VisitSchema()
        data = visit_schema.dump(visit).data
        return data

    # Otherwise, nope, didn't find that visit
    else:
        abort(404, f"Visit not found for Id: {visit_id}")


def create(user_id, visit):
    """
    This function creates a new visit related to the passed in user id.

    :param user_id:       Id of the user the visit is related to
    :param visit:            The JSON containing the visit data
    :return:                201 on success
    """
    # get the parent user
    user = User.query.filter(User.user_id == user_id).one_or_none()

    # Check if the current user has already been assigned a visit which overlaps with the incoming one.
    # To do that, first
    # Convert start_date and end_date strings to timezone-aware datetime first.
    # Assumption: Incoming date from visit is a timezone aware date in string format. 

    form_start_date = visit.get('start_date', '')
    form_end_date = visit.get('end_date', '')

    start_dt = datetime.fromisoformat(form_start_date)

    assigned_vist = Visit.query.filter(Visit.user_id == user_id).filter(start_dt <= Visit.end_date).first()
    if assigned_vist:
        abort(409, f"Sorry user with Id ({user_id}) is not available!")
    

    # Was a user found?
    if user is None:
        abort(404, f"User not found for Id: {user_id}")

    # Create a visit schema instance
    schema = VisitSchema()
    new_visit = schema.load(visit, session=db.session).data

    # Add the visit to the user and database
    user.visits.append(new_visit)
    db.session.commit()

    # Serialize and return the newly created visit in the response
    data = schema.dump(new_visit).data

    return data, 201


def update(user_id, visit_id, visit):
    """
    This function updates an existing visit related to the passed in
    user id.

    :param user_id:       Id of the user the visit is related to
    :param visit_id:         Id of the visit to update
    :param content:            The JSON containing the visit data
    :return:                200 on success
    """
    update_visit = (
        Visit.query.filter(User.user_id == user_id)
        .filter(Visit.visit_id == visit_id)
        .one_or_none()
    )

    # Did we find an existing visit?
    if update_visit is not None:

        # turn the passed in visit into a db object
        schema = VisitSchema()
        update = schema.load(visit, session=db.session).data

        # Set the id's to the visit we want to update
        update.user_id = update_visit.user_id
        update.visit_id = update_visit.visit_id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated visit in the response
        data = schema.dump(update_visit).data

        return data, 200

    # Otherwise, nope, didn't find that visit
    else:
        abort(404, f"Visit not found for Id: {visit_id}")


def delete(user_id, visit_id):
    """
    This function deletes a visit from the visit structure

    :param user_id:   Id of the user the visit is related to
    :param visit_id:     Id of the visit to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the visit requested
    visit = (
        Visit.query.filter(User.user_id == user_id)
        .filter(Visit.visit_id == visit_id)
        .one_or_none()
    )

    # did we find a visit?
    if visit is not None:
        db.session.delete(visit)
        db.session.commit()
        return make_response(
            "Visit {visit_id} deleted".format(visit_id=visit_id), 200
        )

    # Otherwise, nope, didn't find that visit
    else:
        abort(404, f"Visit not found for Id: {visit_id}")
Visit