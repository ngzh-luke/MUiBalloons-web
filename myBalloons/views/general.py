from flask import render_template, Blueprint
from .. import systemInfo
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home/')
@views.route('/index/')
def home(): # level = 0
    return render_template('home_l-d.html', about=systemInfo, user=current_user)

@views.route('/iticketviewer/')
def iTicketViewer(): # level = 0
    return render_template('iticketviewer.html', user=current_user)