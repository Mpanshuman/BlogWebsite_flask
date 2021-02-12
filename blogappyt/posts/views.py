from flask import Blueprint
from blogappyt.posts.forms import  PostForm
from flask import render_template,flash,redirect,url_for,request,abort
from flask_login import current_user
from blogappyt import bcrypt,db, mail
from blogappyt.models import User,Post,Like_Post
from flask_login import login_user,current_user,logout_user,login_required
import secrets
import os
from PIL import Image
from flask_mail import Message

posts = Blueprint('posts', __name__)

@posts.route('/post/new', methods=['GET','POST'])
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
        return redirect(url_for('main.index'))

    return render_template('newpost.html',title ='Create Post',form=form,legend="New Post")

@posts.route('/post/<int:post_id>')
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    post_liked = Like_Post.query.get_or_404(post_id)
    print(post_liked)
    return render_template('post.html',title = post.title,post=post,post_liked=post_liked)

@posts.route('/post/<int:post_id>/update',methods=['GET','POST'])
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
        return redirect(url_for('posts.post',post_id = post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    
    return render_template('newpost.html',title ='Update Post',form=form,legend="Update Post")



@posts.route('/post/<int:post_id>/delete',methods=['GET','POST'])
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
    return redirect(url_for('main.index'))


@posts.route('/likepost/<int:post_id>')
@login_required
def like_post(post_id):
    post_like_counter = Like_Post.query.filter_by(post_id = post_id).first()
    if post_like_counter:
        post_like_counter.like_counter += 1
        db.session.add(post_like_counter)
        db.session.commit()
        return redirect(request.referrer)

@posts.route('/dislikepost/<int:post_id>')
@login_required
def dislike_post(post_id):
    post_dislike_counter = Like_Post.query.filter_by(post_id = post_id).first()
    if post_dislike_counter:
        post_dislike_counter.dislike_counter += 1
        db.session.add(post_dislike_counter)
        db.session.commit()
        return redirect(request.referrer)
