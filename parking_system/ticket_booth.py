from mysql.connector import MySQLConnection, Error
from parking_system.db_dao import get_db
from flask import (
    Blueprint,
    flash,
    render_template,
    request,
    url_for,
    g,
    redirect,
    make_response,
    jsonify,
)
import re
import json
from uuid import uuid1
from datetime import datetime

blueprint = Blueprint(
    "ticket_booth", __name__, url_prefix="/api/v1/ticket-booth"
)


@blueprint.route("/register-car", methods=(["POST"]))
def register_car():
    license_plate = request.json["license_plate"]
    connection_object = get_db("ticket_booth")
    cursor = connection_object.cursor(named_tuple=True)
    duplication_check_query = """SELECT EXISTS(SELECT license_plate FROM Car WHERE license_plate =%s) AS isRegistered"""
    insert_query = """INSERT INTO Car (license_plate) VALUES (%s)"""

    try:
        cursor.execute(duplication_check_query, (license_plate,))
        if cursor.fetchone().isRegistered == 1:
            response = {
                "message": "Car already registered",
                "data": {"license_plate": license_plate},
            }
            return make_response(jsonify(response), 202)
        cursor.execute(insert_query, (license_plate,))
        connection_object.commit()
        response = {
            "message": "Car registered",
            "data": {"owner_id": "", "license_plate": license_plate},
        }
        return make_response(jsonify(response), 201)
    except Error as err:
        connection_object.rollback()
        print("Error Code:", err.errno)
        print("SQLSTATE:", err.sqlstate)
        print("Message:", err.msg)
    except TypeError as err:
        print("No valid json data received\n", err)
    finally:
        cursor.close()


@blueprint.route("/check-in-car", methods=(["POST"]))
def check_in_car_record():
    record_id = uuid1().bytes
    license_plate = request.json["license_plate"]
    space_id = request.json["space_id"]
    check_in_time = datetime.now()
    connection_object = get_db("ticket_booth")

    cursor = connection_object.cursor(named_tuple=True)
    duplication_check_query = """SELECT EXISTS(SELECT record_id FROM CarRecord WHERE license_plate=%s AND check_out IS NULL) AS isRegistered"""
    insert_query = """INSERT INTO CarRecord (record_id, license_plate, space_id, check_in, is_paid) VALUES(%s, %s, %s, %s, 0)"""
    try:
        cursor.execute(duplication_check_query, (license_plate,))
        if cursor.fetchone().isRegistered == 1:
            response = {
                "message": "Car is already checked-in.",
                "data": {"license_plate": license_plate},
            }
            return make_response(jsonify(response), 202)
        cursor.execute(
            insert_query, (record_id, license_plate, space_id, check_in_time)
        )
        connection_object.commit()
        response = {
            "message": "Car record created. Checked in.",
            "data": {
                "record_id": str(record_id),
                "license_plate": license_plate,
                "space_id": space_id,
                "check_in": check_in_time,
            },
        }
        return make_response(jsonify(response), 201)
    except Error as err:
        connection_object.rollback()
        print("Error Code:", err.errno)
        print("SQLSTATE:", err.sqlstate)
        print("Message:", err.msg)
    except TypeError as err:
        print("No valid json data received\n", err)
    finally:
        cursor.close()


@blueprint.route("/check-out-car", methods=(["POST"]))
def check_out_car_record():
    license_plate = request.json["license_plate"]
    check_out_time = datetime.now().replace(microsecond=0)
    print(check_out_time)
    connection_object = get_db("ticket_booth")

    cursor = connection_object.cursor(named_tuple=True)
    update_query = """UPDATE CarRecord SET check_out = %s WHERE license_plate = %s AND check_out IS NULL"""
    select_query = """SELECT * FROM CarRecord WHERE check_out = %s AND license_plate = %s"""
    try:
        cursor.execute(update_query, (check_out_time, license_plate))
        cursor.execute(select_query, (check_out_time, license_plate))
        data = cursor.fetchone()
        connection_object.commit()
        response = {
            "message": "Car record updated. Checked out.",
            "data": {
                "record_id": str(data.record_id),
                "license_plate": data.license_plate,
                "space_id": data.space_id,
                "check_in": data.check_in,
                "check_out": data.check_out,
                "is_paid": data.is_paid,
            },
        }
        return make_response(jsonify(response), 201)
    except Error as err:
        connection_object.rollback()
        print("Error Code:", err.errno)
        print("SQLSTATE:", err.sqlstate)
        print("Message:", err.msg)
    except TypeError as err:
        print("No valid json data received\n", err)
    finally:
        cursor.close()


@blueprint.route("/occupy-space", methods=(["POST"]))
def occupy_parking_space():
    space_id = request.json["space_id"]
    connection_object = get_db("ticket_booth")

    cursor = connection_object.cursor()
    update_query = (
        """UPDATE ParkingSpace SET is_occupied = 1 WHERE space_id = %s"""
    )
    try:
        cursor.execute(update_query, (space_id,))
        connection_object.commit()
        response = {
            "message": "Parking space occupied.",
            "data": {"space_id": space_id},
        }
        return make_response(jsonify(response), 201)
    except Error as err:
        connection_object.rollback()
        print("Error Code:", err.errno)
        print("SQLSTATE:", err.sqlstate)
        print("Message:", err.msg)
    except TypeError as err:
        print("No valid json data received\n", err)
    finally:
        cursor.close()


@blueprint.route("/free-space", methods=(["POST"]))
def free_parking_space():
    space_id = request.json["space_id"]
    connection_object = get_db("ticket_booth")

    cursor = connection_object.cursor()
    update_query = (
        """UPDATE ParkingSpace SET is_occupied = 0 WHERE space_id = %s"""
    )
    try:
        cursor.execute(update_query, (space_id,))
        connection_object.commit()
        response = {
            "message": "Parking space freed.",
            "data": {"space_id": space_id},
        }
        return make_response(jsonify(response), 201)
    except Error as err:
        connection_object.rollback()
        print("Error Code:", err.errno)
        print("SQLSTATE:", err.sqlstate)
        print("Message:", err.msg)
    except TypeError as err:
        print("No valid json data received\n", err)
    finally:
        cursor.close()
