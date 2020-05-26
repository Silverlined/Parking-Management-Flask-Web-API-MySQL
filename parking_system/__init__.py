from os import makedirs
from flask import Flask


def create_app():
    """Create a Flask application

        This file serves two purposes: 
            * Contains the application factory method
            * Tells Python that the "parking_system" directory should be treated as a package
    """

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY="dev")

    # ensure the instance folder exists
    try:
        makedirs(app.instance_path)
    except OSError as error:
        print(error)
        pass

    # a simple page that says hello
    @app.route("/hello")
    def hello():
        return "Hello, World!"

    return app
