from flask            import Flask
from app.config       import Config
from datetime         import datetime 
from sqlalchemy       import create_engine
from flask_bcrypt     import Bcrypt
from flask_login      import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap  import Bootstrap
from flask_datepicker import datepicker

enable_search = True

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    application = Flask(__name__)
    application.config.from_object(Config)
    
    Bootstrap(application)
    datepicker(application)
    
    db.init_app(application)
    bcrypt.init_app(application)
    login_manager.init_app(application)
    
    from app.main.routes import main
    from app.users.routes import users
    from app.tasker.routes import tasker
    
    application.register_blueprint(main)
    application.register_blueprint(users)
    application.register_blueprint(tasker)
    
    return application
