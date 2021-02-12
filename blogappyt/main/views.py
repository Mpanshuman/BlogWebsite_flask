from flask import Blueprint
from flask import render_template,flash,redirect,url_for,request,abort
from flask_login import current_user
from blogappyt import bcrypt,db, mail
from blogappyt.models import User,Post,Like_Post
from flask_mail import Message

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def index():
    # read from url ?page=1
    # request.args.get(arguement,default,type)
    page = request.args.get('page',1,type=int)
    post_likes = Like_Post.query.order_by(Like_Post.date_posted.desc()).all()
    all_post = Post.query.order_by(Post.date_posted.desc()).all()
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
    print(type(Post.query.order_by(Post.date_posted.desc())))
    return render_template('index.html',posts = posts)

@main.route('/about')
def about():
    return render_template('about.html',title='About')
