import os
import json

#with open('/etc/config.json') as cfg_file:
    #config = json.load(cfg_file)

#basedir = os.path.abspath(os.path.dirname(__file__))

#class Config:
    #SECRET_KEY  = config.get('SECRET_KEY')
    #SECURITY_PASSWORD_SALT  = config.get('SECRET_KEY')
    #SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI')
    #SQLALCHEMY_TRACK_MODIFICATIONS = False
    #EMAIL_USER    = config.get('EMAIL_USER')
    #EMAIL_PASS    = config.get('EMAIL_PASS')
    #MAIL_DEFAULT_SENDER='Sender'
    #CSRF_ENABLED = True

class Config:
    CSRF_ENABLED = True
    SECRET_KEY   = 'secret'
    EMAIL_USER   = 'user@gmail.com'
    EMAIL_PASS   = 'mail_password'
    SECURITY_PASSWORD_SALT  = 'keykey'
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_DEFAULT_SENDER='Sender'
