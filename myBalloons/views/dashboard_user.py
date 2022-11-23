from flask import render_template, Blueprint, redirect, url_for
from flask_login import current_user, login_required
from .. import systemInfo


user_dashboard = Blueprint('user_dashboard', __name__)

@user_dashboard.route('/dashboard')
@login_required
def userDashboardURL():
    return redirect(url_for('user_dashboard.userDashboard', user_id=current_user.id))

@user_dashboard.route('/<int:user_id>/dashboard/')
@login_required
def userDashboard(user_id):
    return render_template('dashboard_user.html', about=systemInfo, user=current_user)
