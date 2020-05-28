import click
from flask import current_app, g
from flask.cli import with_appcontext
from mysql.connector import MySQLConnection, Error
from json import load


def read_db_config(filename="dbconfig.json"):
    """Read database configuration data from a json file."""

    config_data = None

    with current_app.open_instance_resource(filename, mode="r") as file:
        config_data = load(file)

    return config_data


def get_db(username):
    """Creates a database connection and ties it to the request object "g". """

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


@click.command("create-tables")
@with_appcontext
def create_tables_command():
    """Flask CLI command to create tables in the database."""

    db_connection = get_db("admin")
    with current_app.open_resource("schema.sql") as f:
        create_query = f.read().decode("utf-8")
        cursor = db_connection.cursor()
        try:
            cursor.execute(create_query, multi=True)
            db_connection.commit()
        except Error as err:
            db_connection.rollback()
            print("Error Code:", err.errno)
            print("SQLSTATE:", err.sqlstate)
            print("Message:", err.msg)
        finally:
            cursor.close()

    click.echo("Initialized the database. Create Tables.")


def init_app(app):
    """Register the `close_db` and `create_tables_command` functions with the application instance."""

    # Tells Flask to call that function when cleaning up after returning the response.
    app.teardown_appcontext(close_db)
    # Adds a new command that can be called with the flask CLI command.
    app.cli.add_command(create_tables_command)
