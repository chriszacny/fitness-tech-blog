from flask import Flask, render_template


application = Flask(__name__)


@application.route('/')
@application.route('/index/')
@application.route('/blog/')
def blog():
    posts = getAllPosts()
    postnavigation = PostNavigation(posts, posts[0])
    return render_template('blog.html', posts=posts, post=posts[0], postnavigation=postnavigation)


def main():
    application.run(host='127.0.0.1', debug=True)


if __name__ == '__main__':
    main()
