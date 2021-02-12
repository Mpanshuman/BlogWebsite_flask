from flask import Blueprint,render_template,flash,redirect,url_for,request,abort
from blogappyt.users.forms import RegistrationForm, LoginForm, UpdateProfileForm, RequestResetForm, ResetpasswordForm
from blogappyt.users.utils import save_picture,password_reset_email
from flask_login import current_user
from blogappyt import bcrypt,db, mail
from blogappyt.models import User,Post,Like_Post
from flask_login import login_user,current_user,logout_user,login_required
import secrets
import os
from PIL import Image
from flask_mail import Message

users = Blueprint('users',__name__)

@users.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email = form.email.data,password= hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Registartion Completed for {form.username.data}!','success')
        return redirect(url_for('users.login'))
    return render_template('registration.html',form=form,title = 'Registration')

@users.route('/login', methods =['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.rememberme.data)
            return redirect(url_for('main.index'))
        else:
            flash('Wrong Info given','danger')
    return render_template('login.html',form=form,title = 'LogIn')

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@users.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        
        # Save Profile Pic
        if form.profilepic.data:
            profile_pic = save_picture(form.profilepic.data)
            current_user.profile_pic = profile_pic
        
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Profile Updated Successfully','success')
        return redirect(url_for('users.profile'))
    
    # Pre-fill the form
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    posts = Post.query.filter_by(auther = current_user)
    profile_pic = url_for('static',filename='profilepic/'+current_user.profile_pic)
    return render_template('profile.html',title ='Profile',profile_pic = profile_pic,form=form,posts=posts)


@users.route('/user/<int:user_id>')
def user_profile(user_id):
    page = request.args.get('page',1,type=int)
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(auther = user).order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
    profile_pic = url_for('static',filename='profilepic/'+user.profile_pic)
    return render_template('user_profile.html',title = user.username,posts=posts,user=user,profile_pic=profile_pic)

@users.route('/reset_password', methods =['GET','POST'])
def request_reset():

    # User needs to be logged out in order to access this page
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            password_reset_email(user)
            flash('A Mail has been sent to your email','success')
            return redirect(url_for('users.login'))
        else:
            flash('This Email is not registered....','warning')
    return render_template('request_reset_form.html',form=form,title = 'Reset Password')


@users.route('/reset_password/<token>', methods =['GET','POST'])
def reset_password(token):

    # User needs to be logged out in order to access this page
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Token is invalid or expired please try agian....','warning')
        return redirect(url_for('users.request_reset'))
    form = ResetpasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your Password has been updated....','success')
        return redirect(url_for('users.login'))
   
    return render_template('reset_password.html',form=form,title = 'Reset Password')