from my_site import application
from my_site import flatpages

from flask import render_template, request, abort
from pygments.formatters import HtmlFormatter
from my_site import posts


@application.route('/')
@application.route('/index/')
@application.route('/home/')
@application.route('/blog/')
def blog():
    parsed_url_arguments = get_parsed_url_arguments()
    model_object_builder = posts.ModelObjectBuilderByCriteria(parsed_url_arguments)
    model_object = model_object_builder.builder_template_method()
    return render_template('blog_posts.html', model_object=model_object)


@application.route('/blog/<slugname>/')
def post(slugname):
    post = get_post_url_by_name(slugname)
    posts = [post]
    return render_template('blog_posts.html', model_object=posts.model_object_builder_by_single_post_name())


@application.route('/about')
def about():
    return render_template('about.html')


# Here is how to get the name of a lexer: pygmentize -N c:\temp\test.bat
# Put that in the MD with :::NAME
@application.route('/pygments.css')
def pygments_css():
    return HtmlFormatter(style='colorful').get_style_defs('.codehilite'), 200, {'Content-Type': 'text/css'}


def get_post_url_by_name(name):
    path = '{}/{}'.format(application.config['BLOG_DIR'], name)
    post = flatpages.get_or_404(path)
    return post


def get_parsed_url_arguments():
    parsed_url_arguments = ParsedUrlArguments()
    builder_workflows = {'page': [validate_page, set_page],
                 'tag': [validate_tag, set_tag],
                 'category': [validate_category, set_category]}
    for key in builder_workflows:
        if key in request.args:
            workflow_to_execute = builder_workflows[key]
            for a_function in workflow_to_execute:
                a_function(parsed_url_arguments)
    return parsed_url_arguments


def validate_page(parsed_url_arguments):
    try:
        int(request.args.get('page'))
    except ValueError:
        abort()


def set_page(parsed_url_arguments):
    parsed_url_arguments.page = int(request.args.get('page'))


def validate_tag(parsed_url_arguments):
    raise NotImplementedError


def set_tag(parsed_url_arguments):
    raise NotImplementedError


def validate_category(parsed_url_arguments):
    raise NotImplementedError


def set_category(parsed_url_arguments):
    raise NotImplementedError


class ParsedUrlArguments:
    def __init__(self, page=0, tag=None, category=None):
        self.page = page
        self.tag = tag
        self.category = category

