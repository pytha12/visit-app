from datetime import datetime
from config import db, ma
from marshmallow import fields


class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(32))
    fname = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    visits = db.relationship(
        "Visit",
        backref="user",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Visit.timestamp)",
    )

    def __repr__(self):
        return f"{self.fname} {self.lname}"


class Visit(db.Model):
    __tablename__ = "visit"
    visit_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    instructions = db.Column(db.String, nullable=True)
    start_date = db.Column(
        db.DateTime, nullable=False
        # db.DateTime, default=datetime.utcnow
    )
    end_date = db.Column(
        db.DateTime, nullable=False
        # db.DateTime, default=datetime.utcnow
    )
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class UserSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    class Meta:
        model = User
        sqla_session = db.session

    visits = fields.Nested("UserVisitSchema", default=[], many=True)


class UserVisitSchema(ma.ModelSchema):
    """
    This class exists to get around a recursion issue
    """

    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    visit_id = fields.Int()
    user_id = fields.Int()
    instructions = fields.Str()
    start_date = fields.Str()
    end_date = fields.Str()
    timestamp = fields.Str()


class DetailVisitSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    class Meta:
        model = Visit
        sqla_session = db.session

    # user = fields.Nested("VisitUserSchema", default=None)


class VisitSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    class Meta:
        model = Visit
        sqla_session = db.session

    user = fields.Nested("VisitUserSchema", default=None)


class VisitUserSchema(ma.ModelSchema):
    """
    This class exists to get around a recursion issue
    """

    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    user_id = fields.Int()
    lname = fields.Str()
    fname = fields.Str()
    timestamp = fields.Str()
