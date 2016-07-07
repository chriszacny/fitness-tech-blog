from flask import Flask, render_template


application = Flask(__name__)


@application.route('/')
@application.route('/index/')
@application.route('/home/')
@application.route('/blog/')
def blog():
    pass


def main():
    application.run(host='127.0.0.1', debug=True)


if __name__ == '__main__':
    main()
