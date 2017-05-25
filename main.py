from flask import Flask
from flask import Blueprint
import secrets

app = Flask(__name__)
app.config['SERVER_NAME'] = 'flask.dev:5000'


@app.route('/')
def hello_world():
    return "<a href=\'"+generate_candidate_url('othertest') + "\'> hello </a>"


def generate_candidate_url(domain):
    return domain + '.flask.dev:5000/' + secrets.token_urlsafe(128)


# Blueprint declaration
bp = Blueprint('subdomain', __name__, subdomain="<user>")


# Add a route to the blueprint
@bp.route("/<user_id>")
def candidate_page(user, user_id):
    return 'Welcome to your subdomain, session number {}'.format(user_id)


@bp.route("/")
def home(user):
    return 'Welcome to your subdomain, user {}'.format(user)


# Register the blueprint into the application
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)
