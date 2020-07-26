from flask import render_template,request,Blueprint,redirect, url_for, flash
from companyblog.models import BlogPost, User, TextOutput, db
from flask_login import current_user
core = Blueprint('core',__name__)

@core.route('/')
def index():
    '''
    This is the home page view. Notice how it uses pagination to show a limited
    number of posts by limiting its query size and then calling paginate.
    '''
    page = request.args.get('page', 1, type=int)
    users = User.query.all()
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=3)
    return render_template('index.html',blog_posts=blog_posts, users=users)

@core.route('/info')
def info():
    '''
    Example view of any other "core" page. Such as a info page, about page,
    contact page. Any page that doesn't really sync with one of the models.
    '''
    return render_template('info.html')

