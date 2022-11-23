from flask import render_template
from flask_login import current_user
from .. import systemInfo

def bad_request(e):
    """Bad request"""
    return render_template("./errorTemplates/400.html", about=systemInfo, user=current_user), 400

def unauthorized(e):
    """Unauthorized access""" # visitor tries to access a restricted web page 
    # but isn’t authorized to do so, usually because of a failed login attempt.
    return render_template("./errorTemplates/401.html", about=systemInfo, user=current_user), 401

def forbidden(e):
    """Forbidden""" # no login opportunity was available
    return render_template("./errorTemplates/403.html", about=systemInfo, user=current_user), 403

def not_found(e):
    """Page not found"""
    return render_template('./errorTemplates/404.html', about=systemInfo, user=current_user), 404

def server_error(e):
    """Internal server error"""
    return render_template("./errorTemplates/500.html", about=systemInfo, user=current_user), 500

def server_down(e):
    """Server down"""
    return render_template("./errorTemplates/503.html", about=systemInfo, user=current_user), 503