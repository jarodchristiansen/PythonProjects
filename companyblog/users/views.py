from flask import render_template ,url_for,flash,redirect,request,Blueprint
import requests
from flask_login import login_user, current_user, logout_user, login_required
from companyblog import db
from companyblog.role_required import admin_required, not_ROLE
from companyblog.models import User, BlogPost, Post, TextOutput
from companyblog.users.forms import RegistrationForm, LoginForm, UpdateUserForm, TextGenForm
from companyblog.users.picture_handler import add_profile_pic


users = Blueprint('users',__name__)

# register

@users.route('/admin')
@admin_required
def view():
    return render_template('view.html')



@users.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(
                    email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    role = 'base')

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registration!')
        return redirect(url_for('users.login'))

    return render_template('register.html',form=form)



# login
@users.route('/login',methods=['GET','POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:

            login_user(user)
            flash('Log in Success!')

            next = request.args.get('next')

            if next ==None or not next[0]=='/':
                next = url_for('core.index')

            return redirect(next)

    return render_template('login.html',form=form)


# logout
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))


# account (update UserForm)
@users.route('/account',methods=['GET','POST'])
@login_required
def account():

    form = UpdateUserForm()
    if form.validate_on_submit():

        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated!')
        return redirect(url_for('users.account'))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static',filename='profile_pics/'+current_user.profile_image)
    text_output = TextOutput.query.order_by(TextOutput.date.desc())
    return render_template('account.html',profile_image=profile_image,form=form, text_output=text_output)

#user's list of blog posts

@users.route('/<username>')
def user_posts(username):
	page = request.args.get('page',1,type=int)
	user = User.query.filter_by(username=username).first_or_404()
	return render_template('user_public_view.html',user=user)




@users.route('/text-generator', methods=['GET', 'POST'])
def textgen():
    form = TextGenForm()

    if form.validate_on_submit():

        seed_text = form.seed_text.data
        r = requests.post(
            "https://api.deepai.org/api/text-generator",
            data={
                'text': seed_text
            },
            headers={'api-key': '9875f94a-9ac3-4000-a0f9-a3700a33d758'}
        )
        flash('Text Submitted')

        output = (r.json()['output'])
        text_output = TextOutput(
                                 text=output,
                                 user_id=current_user.id,
                                 sa_score=0,
                             )
        db.session.add(text_output)
        db.session.commit()
        flash('Text Generated')
        return redirect(url_for('users.account'))

    return render_template('textgen.html', form=form)




