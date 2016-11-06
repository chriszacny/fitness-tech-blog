from flask import Flask, render_template, abort
from flask_flatpages import FlatPages
from pygments.formatters import HtmlFormatter


application = Flask(__name__)
flatpages = FlatPages(application)


@application.route('/')
@application.route('/index/')
@application.route('/home/')
@application.route('/blog/')
def blog():
    return render_template('blog_posts.html', posts=get_all_posts())


@application.route('/blog/<slugname>/')
def post(slugname):
    post = get_post_url_by_name(slugname)
    posts = [post]
    return render_template('blog_posts.html', posts=posts)


@application.route('/blog/tag')
def posts_by_tag(tag_name):
    #TODO Figure this out
    abort(404)


@application.route('/blog/category')
def posts_by_category(category_name):
    #TODO Figure this out
    abort(404)


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


def get_all_posts():
    posts = [p for p in flatpages if p.path.startswith(application.config['BLOG_DIR'])]
    print(posts)
    posts.sort(key=lambda item:item.meta['date'], reverse=True)
    return posts


def main():
    application.config.from_pyfile('settings.py', silent=True)
    flatpages.init_app(application)
    application.run(host=application.config['HOST'], debug=True)


if __name__ == '__main__':
    main()
