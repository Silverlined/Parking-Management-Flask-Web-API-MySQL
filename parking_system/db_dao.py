import click
from flask import current_app, g
from flask.cli import with_appcontext
from mysql.connector import MySQLConnection, Error
from json import load
from collections import namedtuple


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


@click.command("populate-tables")
@with_appcontext
def populate_tables_command():
    """Flask CLI command to populate the parking system tables with data."""

    connection_object = get_db("admin")
    select_parking_lot_capacity = """SELECT capacity_all, capacity_charging from ParkingLot WHERE name = "Zernike P7" """
    insert_parking_spaces = """
                                INSERT INTO ParkingSpace(space_id, lot_id, space_type, sensor_id, is_occupied, hourly_tariff) 
                                    VALUES (%s, (SELECT lot_id FROM ParkingLot LIMIT 1), %s, %s, 0, %s)
                            """
    insert_parking_lot = """INSERT INTO `ParkingLot`(`lot_id`, `name`, `location`, `capacity_all`, `capacity_charging`) VALUES (UUID_TO_BIN(UUID()), "Zernike P7", "Nettelbosje 2, 9747 AD Groningen", 60, 10)"""
    cursor = connection_object.cursor(named_tuple=True)

    try:
        cursor.execute(insert_parking_lot)
        cursor.execute(select_parking_lot_capacity)
        row = cursor.fetchone()
        capacity_all = row.capacity_all
        capacity_charging = row.capacity_charging
        ParkingSpace = namedtuple(
            "ParkingSpace", "space_id space_type sensor_id hourly_tariff"
        )
        for i in range(capacity_all):
            if i < capacity_all - capacity_charging:
                space_data = ParkingSpace(
                    space_id=i,
                    space_type="non_charging",
                    sensor_id=i,
                    hourly_tariff=1.20,
                )
                cursor.execute(insert_parking_spaces, space_data)
            else:
                space_data = ParkingSpace(
                    space_id=i,
                    space_type="charging",
                    sensor_id=i,
                    hourly_tariff=1.32,
                )
                cursor.execute(insert_parking_spaces, space_data)
        print("Executed")
        connection_object.commit()
    except Error as err:
        connection_object.rollback()
        print("Error Code:", err.errno)
        print("SQLSTATE:", err.sqlstate)
        print("Message:", err.msg)
    finally:
        cursor.close()
    click.echo("Populated the database.")
