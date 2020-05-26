import click
from flask import current_app, g
from flask.cli import with_appcontext
from mysql.connector import MySQLConnection, Error
from json import load


def read_db_config(filename="dbconfig.json"):
    config_data = None

    with current_app.open_instance_resource(filename, "r") as file:
        config_data = load(file)

    return config_data


def get_db(username):
    """Creates a database connection and ties it to the request object "g" """

    if "db_connection" not in g:
        config = read_db_config()[username]
        if config is not None:
            try:
                g.db_connection = MySQLConnection(
                    host=config["hostname"],
                    user=config["username"],
                    passwd=config["password"],
                    db=config["database"],
                    auth_plugin="mysql_native_password",
                )
            except Error as err:
                print("Error Code:", err.errno)
                print("SQLSTATE:", err.sqlstate)
                print("Message:", err.msg)
        else:
            print("No configuration data.")
    return g.db_connection


def close_db(e=None):
    db_connection = g.pop("db_connection", None)

    if db_connection is not None:
        db_connection.close()


def init_db():
    db = get_db("admin")

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Create database tables"""

    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
