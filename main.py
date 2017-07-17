"""Python Flask API Auth0 integration example
"""
import bson
from bson import Binary, Code
from bson.json_util import dumps
from bson import json_util
from bson.objectid import ObjectId
import pprint

from functools import wraps
import json
from os import environ as env, path
from urllib.request import urlopen
from db.db_handler import Db_Handler
from dotenv import load_dotenv
from flask import Flask, request, jsonify, _app_ctx_stack, abort
from flask_cors import cross_origin, CORS
from jose import jwt
from engine.send_emails import HandleEmail


def create_app(db):

    load_dotenv(path.join(path.dirname(__file__), ".env"))
    AUTH0_DOMAIN = env["AUTH0_DOMAIN"]
    API_AUDIENCE = env["API_ID"]

    app = Flask(__name__)
    CORS(app)

    # Format error response and append status code.
    def handle_error(error, status_code):
        """Handles the errors
        """
        resp = jsonify({"message": error})
        resp.status_code = status_code
        return resp

    @app.route("/v1.0/accounts", methods=['POST'])
    # if post method it creats an account
    # @cross_origin(headers=["Content-Type", "Authorization"])
    def create_account():
        if request.headers['Content-Type'] != "application/json":
            return handle_error("Content-Type != application/json", 400)
        if not 'email' in request.json:
            return handle_error("No email field in request. Needs {'email': '<test@gmail.com>'}", 400)
        data = request.json
        email = data['email']
        Db_Handler(db).register_user(email, data)
        user_id = str(Db_Handler(db).get_id_from_email(
            email))
        # returns user_id for ease of use
        company = Db_Handler(db).get_company_from_email(email)
        resp = jsonify({"user_id": user_id, "company": company})
        resp.status_code = 201
        return resp

    @app.route("/v1.0/accounts/<user_id>", methods=['GET'])
    # if get method lookup user with __ id
    # @cross_origin(headers=["Content-Type", "Authorization"])
    def lookup_user_by_id(user_id):
        try:
            user_info = Db_Handler(db).lookup_user_by_id(user_id)
        except bson.errors.InvalidId as err:
            return handle_error(str(err), 400)
        if user_info:
            user_info['_id'] = str(user_info['_id'])
        resp = jsonify(user_info)
        resp.status_code = 200
        return resp

    @app.route("/v1.0/answers", methods=['POST'])
    # @cross_origin(headers=["Content-Type", "Authorization"])
    def submit_answers(user_id):
        if request.headers['Content-Type'] != "application/json":
            return handle_error("Content-Type != application/json", 400)
        if 'user_id' or 'text' or 'response' not in request.json:
            return handle_error("Request needs email and text keys.", 400)

        data = request.json()
        user_id = data['user_id']
        text = data['text']
        response = data['response']

        Db_Handler(db).insert_answers(user_id, text, response)
        # return HttpResponse(status=204)

    @app.route("/v1.0/survey/get_questions/", methods=['GET'])
    @app.route("/v1.0/survey/get_questions/<lookup>", methods=['GET'])
    @cross_origin(headers=["Content-Type", "Authorization"])
    # gets questions from first survey
    def get_questions(lookup=None):
        questions = Db_Handler(db).get_survey_questions()
        resp = jsonify(questions)
        resp.status_code = 200
        return resp

    @app.route("/v1.0/survey/companies/<id>", methods=['GET'])
    # gets company from email
    @cross_origin(headers=["Content-Type", "Authorization"])
    def get_company(id):
        company = Db_Handler(db).get_company_from_id(id)
        resp = jsonify({"company": company})
        resp.status_code = 200
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
            jsonurl = urlopen("https://" + AUTH0_DOMAIN +
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
    @app.route("/ping")
    @cross_origin(headers=["Content-Type", "Authorization"])
    def ping():
        """No access token required to access this route
        """
        return "All good. You don't need to be authenticated to call this"

    @app.route("/secured/ping")
    @cross_origin(headers=["Content-Type", "Authorization"])
    @cross_origin(headers=["Access-Control-Allow-Origin", "*"])
    @requires_auth
    def secured_ping():
        """A valid access token is required to access this route
        """
        return "All good. You only get this message if you're authenticated"

    @app.route("/secured/private/ping")
    @cross_origin(headers=["Content-Type", "Authorization"])
    @cross_origin(headers=["Access-Control-Allow-Origin", "*"])
    @requires_auth
    def secured_private_ping():
        """A valid access token and an appropriate scope are required to access this route
        """
        if requires_scope("read:agenda"):
            return "All good. You're authenticated and the access token has the appropriate scope"
        return "You don't have access to this resource"

    @app.route("/secured/api/get_questionnaire")
    @cross_origin(headers=["Content-Type", "Authorization"])
    @cross_origin(headers=["Access-Control-Allow-Origin", "*"])
    # @requires_auth
    def get_questionnaire():
        """Get a survey from database
        """
        questionnaire = Db_Handler(db).get_questionnaire("DeepHire")
        return dumps(questionnaire)

    @app.route("/secured/api/insert_response", methods=['GET', 'POST'])
    @cross_origin(headers=["Content-Type", "Authorization"])
    def insert_response():
        """Insert a survey question response to database
        """
        data = request.get_data().decode('utf-8')

        test = json.loads(data)
        print(test)

        Db_Handler(db).insert_one_response(test)

        for doc in Db_Handler(db).responses.find():
            print(doc)
        HandleEmail().send("russell@deephire.io", test)
        HandleEmail().send("steve@deephire.io", test)
        HandleEmail().send("nick@deephire.io", test)
        return ('{"code":"success"')

    @cross_origin(headers=["Content-Type", "Authorization"])
    @cross_origin(headers=["Access-Control-Allow-Origin", "*"])
    @requires_auth
    def secured_private_ping():
        """A valid access token and an appropriate scope are required to access this route
        """
        if requires_scope("read:agenda"):
            return "All good. You're authenticated and the access token has the appropriate scope"
        return "You don't have access to this resource"

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=env.get("PORT", 3001))
