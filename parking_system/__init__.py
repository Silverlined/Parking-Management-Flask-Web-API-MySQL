from os import makedirs
from flask import Flask
from parking_system import (
    auth,
    users,
    billboard,
    ticket_booth,
    maintenance,
    db_dao,
)
from markdown import markdown
import os


def init_app(app):
    """Register the `close_db` and `create_tables_command` functions with the application instance."""

    app.register_blueprint(auth.blueprint)
    app.register_blueprint(users.blueprint)
    app.register_blueprint(ticket_booth.blueprint)
    app.register_blueprint(billboard.blueprint)
    app.register_blueprint(maintenance.blueprint)

    # Tells Flask to call that function when cleaning up after returning the response.
    app.teardown_appcontext(db_dao.close_db)
    # Adds a new command that can be called with the flask CLI command.
    app.cli.add_command(db_dao.create_tables_command)
    app.cli.add_command(db_dao.populate_tables_command)


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

    init_app(app)

    return app
