from flask import render_template, Blueprint
from .. import systemInfo


user_dashboard = Blueprint('user_dashboard', __name__)

# @user_dashboard.route('/<int:user_id>/dashboard/')

# def userDashboard():
#     return render_template('home_l-d.html', about=systemInfo)
