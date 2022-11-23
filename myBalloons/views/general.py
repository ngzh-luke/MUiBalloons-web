from flask import render_template, Blueprint
from .. import systemInfo
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home/')
@views.route('/index/')
def home():
    return render_template('home_l-d.html', about=systemInfo, user=current_user)
