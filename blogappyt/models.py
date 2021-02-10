from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from blogappyt import db, login_manager, app
from flask_login import UserMixin
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# Database
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key= True)
    username = db.Column(db.String(60),unique = True, nullable = False)
    email = db.Column(db.String(60),unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)
    profile_pic = db.Column(db.String(60), nullable = False,default= 'default.png')
    post = db.relationship('Post',backref = "auther",lazy = True)
    
    def get_reset_token(self,expire_sec = 1800):
        s = Serializer(app.config['SECRET_KEY'],expire_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return '<User %r>' %self.username

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(60),nullable = False)
    date_posted = db.Column(db.DateTime,nullable = False,default = datetime.utcnow)
    content = db.Column(db.Text,nullable = False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' %self.title
