from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_login import LoginManager
from companyblog.role_required import admin_required, redirect_for_insufficient_role
import datetime

app = Flask(__name__)



############## Setting Up Database #####################
_secret_key = os.environ.get("SECRET_KEY")
if not _secret_key:
    raise RuntimeError(
        "SECRET_KEY environment variable must be set. "
        "See .env.example in Flask/Blog (copy to .env or export SECRET_KEY)."
    )
app.config["SECRET_KEY"] = _secret_key
app.permanent_session_lifetime = datetime.timedelta(days=365)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHMEY_TRACK_MODIFICATIONS'] = False
app.config.from_object('companyblog.blogposts.config.Config')
db = SQLAlchemy(app)



Migrate(app,db)


#login configs

LoginManager.redirect_for_insufficient_role = redirect_for_insufficient_role
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.insufficient_role_view = 'core.index'
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