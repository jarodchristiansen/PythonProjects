import os
from PIL import Image
from flask import url_for, current_app


def add_profile_pic(pic_upload, username):
    filename = pic_upload.filename
    ext_type = filename.split('.')[-1]
    storage_filename = str(username) + '.' + ext_type

    filepath = os.path.join(current_app.root_path, 'static\Profile_Pics', storage_filename)

    output_size = (200, 200)

    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)

    return storage_filename


def add_featured_img(pic_upload, meta_title):
    filename = pic_upload.filename
    ext_type = filename.split('.')[-1]
    storage_filename = str(meta_title) + '.' + ext_type
    filepath = os.path.join(current_app.root_path, 'static\Featured_Imgs', storage_filename)
    output_size = (600, 400)
    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)

    return storage_filename