from os import makedirs
from flask import Flask
from parking_system import billboard
from parking_system import auth
from parking_system import db_dao
from markdown import markdown
import os


def create_app():
    """Create a Flask application

        This file serves two purposes: 
            * Contains the application factory method
            * Tells Python that the "parking_system" directory should be treated as a package
    """

    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = "dev"

    # Ensure the instance folder exists
    try:
        if app.instance_path is None:
            makedirs(app.instance_path)
    except OSError as error:
        print(error)
        pass

    @app.route("/")
    def index():
        """Present the project documentation"""

        with open(
            os.path.dirname(app.root_path) + "/README.md", "r"
        ) as markdown_file:
            content = markdown_file.read()
            return markdown(content)

    db_dao.init_app(app)
    app.register_blueprint(auth.blueprint)
    app.register_blueprint(billboard.blueprint)

    return app
