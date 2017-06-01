"""Python Flask API Auth0 integration example
"""

from bson import Binary, Code
from bson.json_util import dumps

from functools import wraps
import json
from os import environ as env, path
import urllib
from db import db_handler

from dotenv import load_dotenv
from flask import Flask, request, jsonify, _app_ctx_stack
from flask_cors import cross_origin
from jose import jwt

load_dotenv(path.join(path.dirname(__file__), ".env"))
AUTH0_DOMAIN = env["AUTH0_DOMAIN"]
API_AUDIENCE = env["API_ID"]

APP = Flask(__name__)


# Format error response and append status code.
def handle_error(error, status_code):
    """Handles the errors
    """
    resp = jsonify(error)
    resp.status_code = status_code
    return resp


def get_token_auth_header():
    """Obtains the access token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        return handle_error({
            "code": "authorization_header_missing",
            "description": "Authorization header is expected"
        }, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        return handle_error({
            "code":
            "invalid_header",
            "description":
            "Authorization header must start with"
            "Bearer"
        }, 401)
    elif len(parts) == 1:
        return handle_error({
            "code": "invalid_header",
            "description": "Token not found"
        }, 401)
    elif len(parts) > 2:
        return handle_error({
            "code":
            "invalid_header",
            "description":
            "Authorization header must be"
            "Bearer token"
        }, 401)

    token = parts[1]
    return token


def requires_scope(required_scope):
    """Determines if the required scope is present in the access token
    Args:
        required_scope (str): The scope required to access the resource
    """
    token = get_token_auth_header()
    unverified_claims = jwt.get_unverified_claims(token)
    token_scopes = unverified_claims["scope"].split()
    for token_scope in token_scopes:
        if token_scope == required_scope:
            return True
    return False


def requires_auth(f):
    """Determines if the access token is valid
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urllib.urlopen("https://" + AUTH0_DOMAIN +
                                 "/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=unverified_header["alg"],
                    audience=API_AUDIENCE,
                    issuer="https://" + AUTH0_DOMAIN + "/")
            except jwt.ExpiredSignatureError:
                return handle_error({
                    "code": "token_expired",
                    "description": "token is expired"
                }, 401)
            except jwt.JWTClaimsError:
                return handle_error({
                    "code":
                    "invalid_claims",
                    "description":
                    "incorrect claims,"
                    "please check the audience and issuer"
                }, 401)
            except Exception:
                return handle_error({
                    "code":
                    "invalid_header",
                    "description":
                    "Unable to parse authentication"
                    "token."
                }, 400)

            _app_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        return handle_error({
            "code": "invalid_header",
            "description": "Unable to find appropriate key"
        }, 400)

    return decorated


# Controllers API
@APP.route("/ping")
@cross_origin(headers=["Content-Type", "Authorization"])
def ping():
    """No access token required to access this route
    """
    return "All good. You don't need to be authenticated to call this"


@APP.route("/secured/ping")
@cross_origin(headers=["Content-Type", "Authorization"])
@cross_origin(headers=["Access-Control-Allow-Origin", "*"])
@requires_auth
def secured_ping():
    """A valid access token is required to access this route
    """
    return "All good. You only get this message if you're authenticated"


@APP.route("/secured/private/ping")
@cross_origin(headers=["Content-Type", "Authorization"])
@cross_origin(headers=["Access-Control-Allow-Origin", "*"])
@requires_auth
def secured_private_ping():
    """A valid access token and an appropriate scope are required to access this route
    """
    if requires_scope("read:agenda"):
        return "All good. You're authenticated and the access token has the appropriate scope"
    return "You don't have access to this resource"


@APP.route("/secured/api/get_questionnaire")
# @cross_origin(headers=["Content-Type", "Authorization"])
# @cross_origin(headers=["Access-Control-Allow-Origin", "*"])
# @requires_auth
def get_questionnaire():
    """Get a survey from database
    """
    questionnaire = db_handler.Db_Handler().get_questionnaire()
    return dumps(questionnaire)


@APP.route("/secured/api/insert_response")
# @cross_origin(headers=["Content-Type", "Authorization"])
# @cross_origin(headers=["Access-Control-Allow-Origin", "*"])
# @requires_auth
def insert_response():
    """Insert a survey question response to database
    """
    data = request.get_json()
    db_handler.Db_Handler().insert_one_response(data)

    for doc in db_handler.Db_Handler().responses.find():
        print(doc)
    return ({"code": "200"})


@cross_origin(headers=["Content-Type", "Authorization"])
@cross_origin(headers=["Access-Control-Allow-Origin", "*"])
@requires_auth
def secured_private_ping():
    """A valid access token and an appropriate scope are required to access this route
    """
    if requires_scope("read:agenda"):
        return "All good. You're authenticated and the access token has the appropriate scope"
    return "You don't have access to this resource"


if __name__ == "__main__":
    APP.run(debug=True, host="0.0.0.0", port=env.get("PORT", 3001))
