from flask import render_template, Blueprint
from .. import systemInfo, systemVersion


auth = Blueprint('auth', __name__)

@auth.route('/sign-up/')
@auth.route('/join-us/')

def signUp():
    return render_template('sign_up.html', systemVersion=systemVersion)

@auth.route('/login/')
def logIn():
    return render_template('login.html', systemVersion =systemVersion)