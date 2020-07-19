from flask import render_template,request,Blueprint,redirect
from companyblog.models import BlogPost
from companyblog.core.forms import TextGenForm
import requests
core = Blueprint('core',__name__)

@core.route('/')
def index():
    '''
    This is the home page view. Notice how it uses pagination to show a limited
    number of posts by limiting its query size and then calling paginate.
    '''
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=10)
    return render_template('index.html',blog_posts=blog_posts)

@core.route('/info')
def info():
    '''
    Example view of any other "core" page. Such as a info page, about page,
    contact page. Any page that doesn't really sync with one of the models.
    '''
    return render_template('info.html')


@core.route('/text-generator')
def textgen():
    form = TextGenForm()

    if form.validate_on_submit():

        seed_text = form.seed_text.data
        import requests
        r = requests.post(
            "https://api.deepai.org/api/text-generator",
            data={
                'text': '{{seed_text}}',
            },
            headers={'api-key': '9875f94a-9ac3-4000-a0f9-a3700a33d758'}
        )
        output = (r.json())
        return redirect('textgen.html', output=output)



    return render_template('textgen.html', form=form)