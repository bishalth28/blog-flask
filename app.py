from flask import Flask, redirect
from flask_smorest import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from db import db
import os
from flask_cors import CORS
from route.user import blp as UserBlueprint
from route.post import blp as PostBlueprint

def create_app():
    app = Flask(__name__)
    app.config["API_TITLE"] = "Auth API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    database_url = os.environ.get("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "super-secret-key-change-in-production"
    CORS(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    api = Api(app)

    api.register_blueprint(UserBlueprint)
    api.register_blueprint(PostBlueprint)

    @app.route("/")
    def root():
        return redirect("/login")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
