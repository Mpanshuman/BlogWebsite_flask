from flask import url_for,current_app
from blogappyt import bcrypt,db, mail
from blogappyt.models import User,Post,Like_Post
import secrets
import os
from PIL import Image
from flask_mail import Message

def save_picture(form_pic):
    random_hex = secrets.token_hex(8)
    f_name,f_ext = os.path.split(form_pic.filename)
    pic_fn = random_hex + f_ext
    pic_path = os.path.join(current_app.root_path,'static/profilepic',pic_fn)
    
    # Resizing Image

    img_size = (125,125)
    i = Image.open(form_pic)
    i.thumbnail(img_size)
    i.save(pic_path)

    return pic_fn

def password_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Link', sender = 'noreply@demo.com',recipients=[user.email])
    msg.body = f'''To Reset Password please visit this link 
    {url_for('users.reset_password',token=token,_external=True)}'''
    mail.send(msg)