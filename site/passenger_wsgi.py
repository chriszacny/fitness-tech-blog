from flask import Flask, render_template
from flask_flatpages import FlatPages


FLATPAGES_AUTO_RELOAD = True
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'content'
BLOG_DIR = 'blog'


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


def get_post_url_by_name(name):
    path = '{}/{}'.format(BLOG_DIR, name)
    post = flatpages.get_or_404(path)
    return post


def get_all_posts():
    posts = [p for p in flatpages if p.path.startswith(BLOG_DIR)]
    posts.sort(key=lambda item:item['date'], reverse=True)
    return posts


def main():
    application.config.from_pyfile('settings.py', silent=True)
    flatpages.init_app(application)
    application.run(host=application.config['HOST'], debug=True)


if __name__ == '__main__':
    main()
