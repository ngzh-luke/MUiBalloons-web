from . import db
from sqlalchemy.sql import func
from flask_security import UserMixin, RoleMixin

# Define models
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(56))
    last_name = db.Column(db.String(56))
    email = db.Column(db.String(156), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default=False)
    phone_country_code = db.Column(db.String(5))
    phone_number = db.Column(db.Integer)
    confirmed_at = db.Column(db.DateTime())
    created_at = db.Column(db.DateTime(), default=func.now())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    points = db.Column(db.Integer, default=0)

    def __str__(self):
        return self.email


class Ticket(db.Model) :
    ticket_id = db.Column(db.Integer, primary_key = True, unique = True) # a referance code for ticket (a key)
    code = db.Column(db.String(10), unique=True) # generator will do just 8 chars, reserved 2 slots for future changes | (a value)
    valid_until = db.Column(db.DateTime(timezone=True))
    issued_date = db.Column(db.DateTime(timezone=True), default=func.now())
    is_apply = db.Column(db.Boolean(), default = False) # the ticket is applied or not
    applied_date = db.Column(db.DateTime(timezone=True), nullable=True)
    issued_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Points(db.Model):
    points_ref_code = db.Column(db.String, primary_key = True, unique = True)
    points_amount = db.Column(db.Integer, default=0)