# blog_posts/views.py
from flask import render_template, url_for, flash, request, redirect, Blueprint, current_app, abort, jsonify
from flask_login import current_user, login_required
import os
from companyblog import db
from companyblog.models import BlogPost, Images
from companyblog.role_required import admin_required, not_ROLE
from companyblog.blogposts.forms import BlogPostForm, PostForm


# blog_posts/views.py

blog_posts = Blueprint('blog_posts', __name__)


# CREATE
@blog_posts.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        blog_post = BlogPost(title=form.heading.data,
                             text=form.post.data,
                             user_id=current_user.id,
                             keywords=form.keywords.data,
                             meta_title=form.meta_title.data,
                             meta_desc=form.meta_desc.data,
                             category=form.category.data,
                             )
        db.session.add(blog_post)
        db.session.commit()
        flash('Blog Post Created')
        return redirect(url_for('core.index'))

    return render_template('create_post.html', form=form)


# BLOG POST (VIEW)
@blog_posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html', title=blog_post.title,
                           date=blog_post.date, post=blog_post, meta_title=blog_post.meta_title,
                           meta_desc=blog_post.meta_desc, category=blog_post.category
                           )


# UPDATE
@blog_posts.route('/<int:blog_post_id>/update', methods=['GET', 'POST'])
@login_required
def update(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        abort(403)

    form = PostForm()

    if form.validate_on_submit():

        blog_post.title = form.heading.data
        blog_post.text = form.post.data
        db.session.commit()
        flash('Blog Post Updated')
        return redirect(url_for('blog_posts.blog_post', blog_post_id=blog_post.id))

    elif request.method == 'GET':
        form.heading.data = blog_post.title
        form.post.data = blog_post.text

    return render_template('create_post.html', title='Updating', form=form)


# DELETE
@blog_posts.route('/<int:blog_post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)

    db.session.delete(blog_post)
    db.session.commit()
    flash('Blog Post Deleted')
    return redirect(url_for('core.index'))


from PIL import Image

# Handles javascript image uploads from tinyMCE
@blog_posts.route('/imageuploader', methods=['POST'])
@login_required
def imageuploader():
    file = request.files.get('file')
    if file:
        filename = file.filename.lower()
        fn, ext = filename.split('.')
        # truncate filename (excluding extension) to 30 characters
        fn = fn[:30]
        filename = fn + '.' + ext
        if ext in ['jpg', 'gif', 'png', 'jpeg']:
            try:
                # everything looks good, save file
                img_fullpath = os.path.join(current_app.config['UPLOADED_PATH'], filename)
                file.save(img_fullpath)
                # get the file size to save to db
                file_size = os.stat(img_fullpath).st_size
                size = 160, 160
                # read image into pillow
                im = Image.open(img_fullpath)
                # get image dimension to save to db
                file_width, file_height = im.size
                # convert to thumbnail
                im.thumbnail(size)
                thumbnail = fn + '-thumb.jpg'
                tmb_fullpath = os.path.join(current_app.config['UPLOADED_PATH_THUMB'], thumbnail)
                # PNG is index while JPG needs RGB
                if not im.mode == 'RGB':
                    im = im.convert('RGB')
                # save thumbnail
                im.save(tmb_fullpath, "JPEG")

                # save to db
                img = Images(filename=filename, thumbnail=thumbnail, file_size=file_size, \
                            file_width=file_width, file_height=file_height)
                db.session.add(img)
                db.session.commit()
            except IOError:
                output = abort(404)
                output.headers['Error'] = 'Cannot create thumbnail for ' + filename
                return output
            return jsonify({'location' : filename})

    # fail, image did not upload
    output = abort(404)
    output.headers['Error'] = 'Filename needs to be JPG, JPEG, GIF or PNG'
    return output