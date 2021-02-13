import os

class Config:
    DEBUG = True
    SECRET_KEY = '7f9cb801c63ff970d98f270084215bb2'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///C:/Users/Anshuman/Desktop/Anshuman_Flask/blogappyt/blogappyt/site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('USER_EMAIL')
    MAIL_PASSWORD = os.environ.get('USER_PASS')
