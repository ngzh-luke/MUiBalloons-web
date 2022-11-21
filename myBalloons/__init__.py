# Root file of the system
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from flask_admin import Admin, BaseView, expose
from flask_security import SQLAlchemyUserDatastore, Security
from flask_login import LoginManager
from flask import Flask, Blueprint, render_template
from .database import User, Role
import os


DB_NAME = "myBalloons_database.sqlite"

def create_app():
    app = Flask(__name__)
    app.config['FLASK_ADMIN-SWATCH'] = 'cerulean'
    app.config['SECRET_KEY'] = '' # To be changed to en characters of when deploy
    app.config['DATABASE_NAME'] = DB_NAME
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # from .account import account
    
    # from .auth import auth
    # from .master_tools import MTs
    # from .models import User, Participant, Ticket, Login_log, Note

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
    app.register_blueprint(rootView, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')
    # app.register_blueprint(account, url_prefix='/')
    # app.register_blueprint(MTs, url_prefix='/')

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Setup Flask-Security
        user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        security = Security(app, user_datastore)

    # with app.app_context(): # Drop all of the tables
    #     db.drop_all()

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

systemInfoObject = About(version=0.132, status='Initial Development#1.4',
                         build=20221121, version_note='Home page view added')
systemInfo = systemInfoObject.__repr__()
systemVersion = systemInfoObject.getSystemVersion()

rootView = Blueprint('rootView', __name__)
@rootView.route("/..root-template-view/")
def root_view():
    return render_template("base.html", about=systemInfo)
