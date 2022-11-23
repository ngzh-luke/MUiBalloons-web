from flask import render_template, Blueprint, redirect, url_for
from .. import systemInfo
from flask_login import login_required, current_user

admin_dashboard = Blueprint('admin_dashboard', __name__)

@admin_dashboard.route('master-tools/dashboard')
@login_required
def adminDashboardURL():
    return redirect(url_for('admin_dashboard.adminDashboard', user_id=current_user.id))

@admin_dashboard.route('/<int:user_id>/master-tools/dashboard/')
@login_required
def adminDashboard(user_id):
    return render_template('dashboard_admin.html', about=systemInfo, user = current_user)

