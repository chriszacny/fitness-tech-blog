from my_site import application

from flask import render_template, request, abort
from pygments.formatters import HtmlFormatter
from my_site import posts
from my_site import model_object

@application.route('/')
@application.route('/index/')
@application.route('/home/')
@application.route('/blog/')
def blog():
    page = 0
    if request.args.get('page') is not None:
        page = request.args.get('page')
    summary_model_object = model_object.SummaryModelObject(page=page)
    return render_template('blog_posts.html', model_object=summary_model_object)


@application.route('/blog/<slugname>/')
def single_blog_post(slugname):
    single_blog_post_model_object = model_object.SingleBlogPostModelObject(slugname)
    return render_template('blog_post.html', model_object=single_blog_post_model_object)


@application.route('/about')
def about():
    return render_template('about.html')


# Here is how to get the name of a lexer: pygmentize -N c:\temp\test.bat
# Put that in the MD with :::NAME
@application.route('/pygments.css')
def pygments_css():
    return HtmlFormatter(style='colorful').get_style_defs('.codehilite'), 200, {'Content-Type': 'text/css'}
