from companyblog import db, login_manager, app
from flask_login import UserMixin, AnonymousUserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_security import  SQLAlchemyUserDatastore, RoleMixin
from hashlib import md5
from flask_migrate import Migrate


#class Admin(db.Model):
 #   _tablename_ = "admins"
 #   id = db.Column(db.Integer, primary_key=True)
 #   name = db.Column(db.String(80), unique=True)
 #   user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
 #   def __repr__(self):
  #      return "<Admin: {}>".format(self.id)

#class Member(db.Model):
 #   _tablename_ = "members"
 #   id = db.Column(db.Integer, primary_key=True)
 #   name = db.Column(db.String(80), unique=True)
 #   user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
 #   def __repr__(self):
 #       return "<Member: {}>".format(self.id)

#class Base(db.Model):
#    _tablename_ = "base"
#    id = db.Column(db.Integer(), primary_key=True)
#    name = db.Column(db.String(80), unique=True)
#    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
#    def __repr__(self):
#        return "<Base: {}>".format(self.id)

 #   def __repr__(self):

  #      return self.id


class Admin(db.Model, UserMixin):
    # RoleUser has role set to the string 'ROLE'.
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    role = 'admin'
    def __repr__(self):
        return "<Admin: {}>".format(self.id)

    def __repr__(self):
        return self.id

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, unique=True,  primary_key=True)
    profile_image = db.Column(db.String(64), nullable=False, default='default.png')
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    admins = db.relationship("Admin", backref="user", lazy="dynamic")
    #teachers = db.relationship("Member", backref="user", lazy="dynamic")
    #students = db.relationship("Base", backref="user", lazy="dynamic")
    posts = db.relationship('BlogPost', backref='author', lazy=True)

    def __init__(self, id, email, username, password, admins):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Username {self.username}"

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)


class Post(db.Model):
    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True)
    #meta_title = db.Column(db.String(60), nullable=False)
    #meta_desc = db.Column(db.String(160), nullable=False)
    #category = db.Column(db.String(160), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    heading = db.Column(db.String(140),nullable=False)
    post = db.Column(db.Text,nullable=False)


class BlogPost(db.Model):
    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True)
    #meta_title = db.Column(db.String(60),nullable=False)
    #meta_desc = db.Column(db.String(160), nullable=False)
    #category = db.Column(db.String(160), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140),nullable=False)
    text = db.Column(db.Text,nullable=False)

    def __init__(self,title,text,user_id):
	    self.title = title
	    self.text = text
	    self.user_id = user_id

    def __repr__(self):
	    return f"Post ID: {self.id}"



db.create_all()

db = SQLAlchemy(app)
migrate = Migrate(app, db)

#security = Security(app, user_datastore)


