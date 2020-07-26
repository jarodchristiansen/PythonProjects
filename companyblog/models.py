from companyblog import db, login_manager, app
from flask_login import UserMixin, AnonymousUserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
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





class Images(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50), nullable=False)
    thumbnail = db.Column(db.String(50), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    file_width = db.Column(db.Integer, nullable=False)
    file_height = db.Column(db.Integer, nullable=False)
    create_date = db.Column(db.DateTime,default=datetime.utcnow, nullable=False)

    def getImage(image_id):
        return Images.query.filter_by(id=image_id).first()


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, unique=True,  primary_key=True)
    profile_image = db.Column(db.String(64), nullable=False, default='default.png')
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(80))
    #teachers = db.relationship("Member", backref="user", lazy="dynamic")
    #students = db.relationship("Base", backref="user", lazy="dynamic")
    posts = db.relationship('BlogPost', backref='author', lazy=True)

    def __init__(self, email, username, password, role):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self. role = role

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
    meta_title = db.Column(db.String(60), nullable=False)
    meta_desc = db.Column(db.String(160), nullable=False)
    category = db.Column(db.String(160), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    heading = db.Column(db.String(140),nullable=False)
    post = db.Column(db.Text,nullable=False)


class BlogPost(db.Model):
    users = db.relationship(User)
    id = db.Column(db.Integer, primary_key=True)
    meta_title = db.Column(db.String(60),nullable=False)
    meta_desc = db.Column(db.String(160), nullable=False)
    category = db.Column(db.String(160), nullable=False)
    keywords = db.Column(db.String(160), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140),nullable=False)
    text = db.Column(db.Text,nullable=False)

    def __init__(self,title,text,user_id, meta_title, meta_desc, category, keywords):
        self.title = title
        self.text = text
        self.user_id = user_id
        self.meta_title = meta_title
        self.meta_desc = meta_desc
        self.category = category
        self.keywords = keywords
    def __repr__(self):
	    return f"Post ID: {self.id}"

class TextOutput(db.Model):
    users = db.relationship(User)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000))
    sa_score = db.Column(db.Integer)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, text, user_id, sa_score):
        self.user_id = user_id
        self.text = text
        self.sa_score = sa_score




db.create_all()

db = SQLAlchemy(app)
migrate = Migrate(app, db)

#security = Security(app, user_datastore)


