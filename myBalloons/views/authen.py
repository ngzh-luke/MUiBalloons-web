from flask import render_template, Blueprint, request, flash, redirect, url_for, session, abort
from .. import systemInfo, systemVersion, db
from flask_login import login_user, login_required, logout_user, current_user
from flask_bcrypt import generate_password_hash, check_password_hash
from ..models import User, TheKeys

auth = Blueprint('auth', __name__)


@auth.route('/logout')
# auth.route('/logout/')
@login_required
def logOut():
    logout_user()
    return render_template('logout.html', user=current_user)


@auth.route('/login/', methods=["POST", "GET"])
def logIn():
   
    try:
        if User.get_id(current_user):
            flash('You are already logged in!', category='info')
            return redirect(url_for("user_dashboard.userDashboard", user_id=current_user.id))
    except:
        pass
    if request.method == 'POST' :
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user :
            if check_password_hash(user.password, password) : # comparing two given parameters
                flash('Logged in Successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Password or the username (Email address) is incorrect!", category= 'error')
        else:
            flash("Password or the username (Email address) is incorrect!", category= 'error') 
    
    return render_template('login.html', systemVersion =systemVersion, about=systemInfo, user=current_user)




@auth.route('/sign-up/', methods = ['GET', 'POST'])
@auth.route('/join-us/', methods = ['GET', 'POST'])
def signUp():

    try:
        if User.get_id(current_user):
            flash('You already have an account!', category='info')
            return redirect(url_for("user_dashboard.userDashboard", user_id=current_user.id))
    except:
        pass
    if request.method == 'POST' :
        theKey = request.form.get('mk')
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        question = request.form.get('security_question')
        answer = request.form.get('security_question_answer')
        k = TheKeys.query.filter_by(key=theKey).first()
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email is already exit!", category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2 :
            flash('Password don\'t match!', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 character.', category='error')
        elif k and (k.is_applied is False): # Master Key is correct
            flash('You are creating the account that has admin role.', category='info')
            try:
                new_user = User(email =email, fname = firstName, 
                password=generate_password_hash(password1).decode('utf-8'),
                role_level=1, master_key_applied=theKey, s_question=question, 
                s_answer=answer ) # admin account
                db.session.add(new_user)
                db.session.commit()
                k.is_applied = True
                # db.session.delete(k)
                db.session.commit()
                # key_to_update = TheKeys(key=key_to_update, is_applied=True)
                # db.session.add(key_to_update)
                # db.session.commit()
                flash('Account created successfully!', category='success')
                return redirect(url_for('auth.logIn'))
            except:
                flash('There is a problem updating the data, please try again later', category='error')
                abort(500)
        elif not k or (k.is_applied is True): # Master Key is incorrect
           flash('Master Key is incorrect! If you are not applying for admin role account, please leave the master key field blank', category='error')
            
            
        else:
            try:
                new_user = User(email =email, fname = firstName, 
                password=generate_password_hash(password1).decode('utf-8'), s_question=question, s_answer=answer) # user account
                db.session.add(new_user)
                db.session.commit()
                flash('Account created successfully!', category='success')
                return redirect(url_for('auth.logIn'))
            except:
                flash('There is a problem updating the data, please try again later', category='error')
                abort(500)
            
    return render_template('sign_up.html', systemVersion=systemVersion, about=systemInfo, user=current_user)


