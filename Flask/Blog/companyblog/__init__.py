from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_login import LoginManager
from companyblog.role_required import admin_required, not_ROLE
import datetime

app = Flask(__name__)



############## Setting Up Database #####################
app.config['SECRET_KEY'] = 'mysecret'
app.permanent_session_lifetime = datetime.timedelta(days=365)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHMEY_TRACK_MODIFICATIONS'] = False
app.config.from_object('companyblog.blogposts.config.Config')
db = SQLAlchemy(app)



Migrate(app,db)


#login configs

LoginManager.not_ROLE = not_ROLE
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.not_ROLE_view = 'core.index'
login_manager.login_view = 'users.login'



from companyblog.core.views import core
from companyblog.users.views import users
from companyblog.error_pages.handlers import error_pages
from companyblog.blogposts.views import blog_posts
from wtf_tinymce import wtf_tinymce




app.register_blueprint(error_pages)
app.register_blueprint(users)
app.register_blueprint(core)
app.register_blueprint(blog_posts)

wtf_tinymce.init_app(app)