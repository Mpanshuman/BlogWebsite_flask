from .forms import RegistrationForm, LoginForm, UpdateProfileForm, PostForm, RequestResetForm, ResetpasswordForm
from flask import render_template,flash,redirect,url_for,request,abort
from flask_login import current_user
from blogappyt import app,bcrypt,db, mail
from blogappyt.models import User,Post,Like_Post
from flask_login import login_user,current_user,logout_user,login_required
import secrets
import os
from PIL import Image
from flask_mail import Message

# Routes

@app.route('/')
@app.route('/home')
def index():
    # read from url ?page=1
    # request.args.get(arguement,default,type)
    page = request.args.get('page',1,type=int)
    post_likes = Like_Post.query.order_by(Like_Post.date_posted.desc()).all()
    all_post = Post.query.order_by(Post.date_posted.desc()).all()
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
    print(type(Post.query.order_by(Post.date_posted.desc())))
    return render_template('index.html',posts = posts)

@app.route('/about')
def about():
    return render_template('about.html',title='About')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email = form.email.data,password= hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Registartion Completed for {form.username.data}!','success')
        return redirect(url_for('login'))
    return render_template('registration.html',form=form,title = 'Registration')

@app.route('/login', methods =['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.rememberme.data)
            return redirect(url_for('index'))
        else:
            flash('Wrong Info given','danger')
    return render_template('login.html',form=form,title = 'LogIn')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Hash profile pic name and save it at static/profilepic folder
def save_picture(form_pic):
    random_hex = secrets.token_hex(8)
    f_name,f_ext = os.path.split(form_pic.filename)
    pic_fn = random_hex + f_ext
    pic_path = os.path.join(app.root_path,'static/profilepic',pic_fn)
    
    # Resizing Image

    img_size = (125,125)
    i = Image.open(form_pic)
    i.thumbnail(img_size)
    i.save(pic_path)

    return pic_fn

@app.route('/profile', methods=['GET','POST'])
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
        return redirect(url_for('profile'))
    # Pre-fill the form
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    posts = Post.query.filter_by(auther = current_user)
    profile_pic = url_for('static',filename='profilepic/'+current_user.profile_pic)
    return render_template('profile.html',title ='Profile',profile_pic = profile_pic,form=form,posts=posts)


@app.route('/post/new', methods=['GET','POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data,content = form.content.data,auther = current_user)
        db.session.add(post)
        db.session.commit()
        print('post_id:',post.id)
        post_liked = Like_Post(post_id = post.id,post_likes = post)
        db.session.add(post_liked)
        db.session.commit()
        flash('Your Blog is Posted...','success')
        return redirect(url_for('index'))

    return render_template('newpost.html',title ='Create Post',form=form,legend="New Post")

@app.route('/post/<int:post_id>')
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    post_liked = Like_Post.query.get_or_404(post_id)
    print(post_liked)
    return render_template('post.html',title = post.title,post=post,post_liked=post_liked)

@app.route('/post/<int:post_id>/update',methods=['GET','POST'])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()
    if post.auther != current_user:
        abort(403)

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your Post has been updated...','success')
        return redirect(url_for('post',post_id = post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    
    return render_template('newpost.html',title ='Update Post',form=form,legend="Update Post")



@app.route('/post/<int:post_id>/delete',methods=['GET','POST'])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    post_liked = Like_Post.query.get_or_404(post_id)
    if post.auther != current_user:
        abort(403)
    db.session.delete(post)
    db.session.delete(post_liked)
    db.session.commit()
    flash('Your Post has been deleted...','success')
    return redirect(url_for('index'))

@app.route('/user/<int:user_id>')
def user_profile(user_id):
    page = request.args.get('page',1,type=int)
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(auther = user).order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
    profile_pic = url_for('static',filename='profilepic/'+user.profile_pic)
    return render_template('user_profile.html',title = user.username,posts=posts,user=user,profile_pic=profile_pic)


def password_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Link', sender = 'noreply@demo.com',recipients=[user.email])
    msg.body = f'''To Reset Password please visit this link 
    {url_for('reset_password',token=token,_external=True)}'''
    mail.send(msg)

@app.route('/reset_password', methods =['GET','POST'])
def request_reset():

    # User needs to be logged out in order to access this page
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            password_reset_email(user)
            flash('A Mail has been sent to your email','success')
            return redirect(url_for('login'))
        else:
            flash('This Email is not registered....','warning')
    return render_template('request_reset_form.html',form=form,title = 'Reset Password')


@app.route('/reset_password/<token>', methods =['GET','POST'])
def reset_password(token):

    # User needs to be logged out in order to access this page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Token is invalid or expired please try agian....','warning')
        return redirect(url_for('request_reset'))
    form = ResetpasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your Password has been updated....','success')
        return redirect(url_for('login'))
   
    return render_template('reset_password.html',form=form,title = 'Reset Password')

@app.route('/likepost/<int:post_id>')
@login_required
def like_post(post_id):
    post_like_counter = Like_Post.query.filter_by(post_id = post_id).first()
    if post_like_counter:
        post_like_counter.like_counter += 1
        db.session.add(post_like_counter)
        db.session.commit()
        return redirect(request.referrer)

@app.route('/dislikepost/<int:post_id>')
@login_required
def dislike_post(post_id):
    post_dislike_counter = Like_Post.query.filter_by(post_id = post_id).first()
    if post_dislike_counter:
        post_dislike_counter.dislike_counter += 1
        db.session.add(post_dislike_counter)
        db.session.commit()
        return redirect(request.referrer)
