from flask import render_template, Blueprint
from .. import systemInfo


admin_dashboard = Blueprint('admin_dashboard', __name__)

# @admin_dashboard.route('/<int:user_id>/master-tools/dashboard')

# def adminDashboard():
#     return render_template('home_l-d.html', about=systemInfo)
