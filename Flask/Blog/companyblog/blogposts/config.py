import os
from dotenv import load_dotenv
from pathlib import Path


basedir = Path(__file__).parent
load_dotenv(basedir / '.env')


class Config(object):

    # tinyMCE settings
    UPLOADED_PATH = os.path.join(basedir,'app/static/uploads')
    UPLOADED_PATH_THUMB = os.path.join(basedir,'app/static/uploads/thumbnails')