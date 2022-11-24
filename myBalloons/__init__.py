# Root file of the system
# from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
# from flask_admin import Admin, BaseView, expose
# from flask_security import Security, SQLAlchemyUserDatastore
from flask_bcrypt import Bcrypt, generate_password_hash
from flask_login import LoginManager, current_user
from flask import Flask, Blueprint, render_template, abort, flash
from .models import User, TheKeys
from decouple import config as en_var # import the environment var
# from werkzeug.exceptions import HTTPException

DB_NAME = "myBalloons_database.sqlite"

def create_app():
    app = Flask(__name__)
    f_bcrypt = Bcrypt(app)
    app.config['FLASK_ADMIN-SWATCH'] = 'cerulean'
    app.config['SECRET_KEY'] = en_var('myBalloonsAppSecretKey') # Encrepted with Environment Variable
    app.config['DATABASE_NAME'] = DB_NAME
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TIMEZONE'] = 'Asia/Bangkok'
    # app.config['SECURITY_TRACKABLE'] = True
    # app.config['SECURITY_CONFIRMABLE'] = True
    # app.config['SECURITY_REGISTER_URL'] = '/sign-up/'
    # app.config['SECURITY_LOGIN_URL'] = '/login/'
    # app.config['SECURITY_LOGOUT_URL'] = '/logout/'
    # app.config['SECURITY_RESET_URL'] = ''
    
    db.init_app(app)

    # from .account import account
    
    # from .master_tools import MTs

    # admin = Admin(app, name='MU iBalloons Database Manager', template_mode='bootstrap3')
    # admin.add_view(ModelView(User, db.session))
    # admin.add_view(ModelView(Login_log, db.session))
    # admin.add_view(ModelView(Ticket, db.session))
    # admin.add_view(ModelView(Note, db.session))
    # admin.add_view(ModelView(Participant, db.session)) 
    from .views.errorHandling import not_found, server_error, bad_request, forbidden, unauthorized, server_down
    app.register_error_handler(400, bad_request)
    app.register_error_handler(401, unauthorized)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, not_found)
    app.register_error_handler(500, server_error)
    app.register_error_handler(503, server_down)

    from .views.general import views
    from .views.authen import auth
    from .views.dashboard_admin import admin_dashboard
    from .views.dashboard_user import user_dashboard
    app.register_blueprint(rootView, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin_dashboard, url_prefix='/')
    app.register_blueprint(user_dashboard, url_prefix='/')

    with app.app_context(): # Drop all of the tables
        db.drop_all()

    with app.app_context():
        db.create_all()


    @app.before_first_request
    def demo_account():
        # createAdminRole = Role(id=1,name="admin")
        # createUserRole = Role(id=0,name="user")
        # db.session.add_all([createAdminRole, createUserRole])
        # db.session.commit()
        try:

            k1 = TheKeys(key='master')
            k2 = TheKeys(key='admin')
            d1 = User(email="demo@admin.com", fname="Admin", lname="Admin Lastname", password=generate_password_hash("admin").decode('utf-8'), role_level=1, s_question='question', s_answer='answer')
            d2 = User(email='demo@user.com',fname="User", lname="User Lastname", password=generate_password_hash("user").decode('utf-8'),s_question='question', s_answer='answer')    
            db.session.add_all([k1,k2,d1, d2])
            db.session.commit()
        except Exception as e:
            flash(f'{e}', category='error')
            

    login_manager = LoginManager()
    login_manager.login_view = 'auth.logIn'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # # Setup Flask-Security
    # user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    # security = Security(app, user_datastore)
    
    
    # @app.before_first_request
    # def create_user():
    #     db.create_all()
    #     user_datastore.create_user(email='matt@nobien.net', password='password')
    #     db.session.commit()




    return app

class About():
    version = float()
    status = str()
    build = int()
    version_note = str()

    def __init__(self, version: float = float(0.0), status: str = 'None Stated', build: int = 20221100, version_note: str = "None Stated"):
        self.version = version
        self.status = status
        self.build = build
        self.version_note = version_note

    def __repr__(self) -> str:
        return str("{ " + f"Version: {self.version} | Status: {self.status} | Build: {self.build} | Details: {self.version_note}" + " }")

    def getSystemVersion(self) -> str:
        return str(self.version)

systemInfoObject = About(version=0.142, status='Initial Development#5',
                         build=20221124, version_note='Sign-up form view customized, iTicketViewer interface added, and added brief login credential on navbar and navbar menu')
systemInfo = systemInfoObject.__repr__()
systemVersion = systemInfoObject.getSystemVersion()

rootView = Blueprint('rootView', __name__)
@rootView.route("/..root-template-view/")
def root_view():
    return render_template("base.html", about=systemInfo, user=current_user)

# Initial Development#5: Sign-up form view customized, iTicketViewer interface added, and added brief login credential on navbar and navbar menu on Novenber 24, 2022 -> 0.142