from . import db
# from sqlalchemy.sql import func
from flask_login import UserMixin, current_user
from datetime import datetime
import pytz

""" # Define models
# roles_users = db.Table(
#     'roles_users',
#     db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
#     db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
# )


# class Role(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(80), unique=True)
#     description = db.Column(db.String(255))

#     def __str__(self):
#         return self.name """


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(156), unique=True)
    fname = db.Column(db.String(56), default=email)
    lname = db.Column(db.String(56), default="Null")
    student_id = db.Column(db.String(10), nullable=True)
    password = db.Column(db.String())
    active = db.Column(db.Boolean(), default=False)
    phone_country_code = db.Column(db.String(5))
    phone_number = db.Column(db.Integer)
    bdate = db.Column(db.DateTime(timezone=True), nullable = True)
    #confirmed_at = db.Column(db.DateTime(timezone=True))
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now(pytz.timezone('Asia/Bangkok')))
    # roles = db.relationship('Role', secondary=roles_users,
                            #  backref=db.backref('users', lazy='dynamic'))
    points = db.relationship('Points',backref=db.backref('users'))
    ticket = db.relationship('Ticket')
    # total_points = db.Column(db.Integer, default=0)
    role_level = db.Column(db.Integer, default=0,nullable=False) # 0 = user, 1 = admin, 2 = super-admin (not defined yet)
    master_key_applied = db.Column(db.String(), nullable=True)
    s_question = db.Column(db.String(), nullable=False)
    s_answer = db.Column(db.String(), nullable =False)
    # profile_pic = db.Column(db.String(), nullable=True)
    college_abbriviation = db.Column(db.String(5), nullable =False, default='MU')
    remarks = db.Column(db.String(), nullable=True)

    """ # def __init__(self, email, password, fname='', lname='', role:list=['user'], phone_country_code='+66'):
    #     self.fname = fname
    #     self.lname = lname
    #     self.created_at = func.now()
    #     self.email = email
    #     self.password = password
    #     for r in role :
    #         if self.theRoles.count(r) == 0:
    #             self.theRoles.append(r)
    #     if self.theRoles.count('user') == 0:
    #         self.theRoles.append('user')


    # def addAdmin(self):
    #     if self.theRoles.count('admin') > 0 :
    #         pass
    #     else:
    #         self.theRoles.append('admin')

    # @property
    # def isAdmin(self) -> bool:
    #     if not current_user.is_authenticated:
    #         # return current_app.login_manager.unauthorized()
    #         return False
    #     elif current_user.is_authenticated and (self.theRoles.count('admin')>0) :
    #         return True """

    @property
    def isAdmin(self) -> bool:
        if not current_user.is_authenticated:
            # return current_app.login_manager.unauthorized()
            return False
        elif current_user.is_authenticated and (current_user.role_level>0 or current_user.role_level==1) :
            return True
        return False

    @property
    def roleRepr(self):
        if self.role_level == 1 :
            return "Admin"
        elif self.role_level == 0 :
            return "User"
        else:
            return "Anonymous"
    


    def __str__(self):
        return self.email


class Ticket(db.Model) :
    ticket_id = db.Column(db.Integer, primary_key = True, unique = True) # a referance code for ticket (a key)
    code = db.Column(db.String(10), unique=True) # generator will do just 8 chars, reserved 2 slots for future changes | (a value)
    valid_until = db.Column(db.DateTime(timezone=True))
    issued_date = db.Column(db.DateTime(timezone=True), default=datetime.now(pytz.timezone('Asia/Bangkok')))
    is_apply = db.Column(db.Boolean(), default = False) # the ticket is applied or not
    applied_date = db.Column(db.DateTime(timezone=True), nullable=True)
    issued_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Points(db.Model):
    points_ref_code = db.Column(db.String(), primary_key = True, unique = True)
    points_amount = db.Column(db.Integer, default=0)
    give_points_to = db.Column(db.Integer, db.ForeignKey('user.id'))


class TheKeys(db.Model) :
    key = db.Column(db.String(), primary_key=True, unique=True, nullable=False)
    is_applied = db.Column(db.Boolean(), default=False, nullable=False)



class Notifications(db.Model) :
    id = db.Column(db.Integer, unique=True, primary_key=True) # notification id
    noti_type = db.Column(db.Integer, nullable=False) # 1XX = System messages
    message = db.Column(db.String(), nullable=False)

