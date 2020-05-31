from mysql.connector import MySQLConnection, Error
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
    abort,
)
import re
import json
from uuid import UUID
from parking_system.db_dao import get_db
from parking_system.auth import login_required
from calendar import month_name


blueprint = Blueprint("maintenance", __name__, url_prefix="/api/v1/maintenance")


@blueprint.route("/sensor-alert", methods=(["GET"]))
def sensor_alert():
    connection_object = get_db("maintenance_app")
    cursor = connection_object.cursor(named_tuple=True)
    select_query = """SELECT COUNT(IF(is_occupied = 1, 1, NULL)) 'detected',
                            COUNT(IF(check_out IS NULL, 1, NULL)) 'parked'
                                FROM (
                                    SELECT r.check_out, ps.is_occupied 
                                        FROM CarRecord r 
                                            INNER JOIN ParkingSpace ps 
                                                USING(space_id)) r_ps
                        """
    try:
        cursor.execute(select_query)
        data = cursor.fetchone()
        if data.detected != data.parked:
            alert = True
        else:
            alert = False
        response = {"message": "Sensor alert", "data": alert}
        return make_response(jsonify(response), 200)
    except Error as err:
        print("Error Code:", err.errno)
        print("SQLSTATE:", err.sqlstate)
        print("Message:", err.msg)
    finally:
        cursor.close()


@blueprint.route("/list-cars", methods=(["GET"]))
def get_currently_parked_cars():
    with_owner = request.args.get("with-owner")
    connection_object = get_db("maintenance_app")
    cursor = connection_object.cursor(named_tuple=True)
    if with_owner == "1":
        select_query = """SELECT
                            rc.license_plate, rc.brand_name, o.first_name, o.surname, rc.space_id, rc.check_in, o.discount_rate
                        FROM
                            (
                            SELECT r.license_plate, c.brand_name, c.owner_id, r.space_id, r.check_in
                            FROM
                                CarRecord r
                            INNER JOIN Car c 
                                ON r.license_plate = c.license_plate AND r.check_out is NULL
                        ) rc
                        LEFT JOIN CarOwner o USING(owner_id)"""
    else:
        select_query = """
                            SELECT r.license_plate, c.brand_name, c.fuel_type
                            FROM
                                CarRecord r
                            INNER JOIN Car c 
                                ON r.license_plate = c.license_plate AND r.check_out is NULL
                        """
    try:
        cursor.execute(select_query)
        rows = cursor.fetchall()
        data = {}
        for index, row in enumerate(rows):
            invoice = {}
            for j in [{i[0]: str(i[1])} for i in list(row._asdict().items())]:
                invoice.update(j)
            data.update({index: invoice})
        response = {
            "message": "List of all the cars parked at the moment",
            "data": data,
        }
        return make_response(jsonify(response), 200)
    except Error as err:
        print("Error Code:", err.errno)
        print("SQLSTATE:", err.sqlstate)
        print("Message:", err.msg)
    finally:
        cursor.close()


@blueprint.route("/overview-cars", methods=(["GET"]))
def overview_amount_cars():
    grouped_by = request.args.get("group-by")
    connection_object = get_db("maintenance_app")
    select_query = None
    if grouped_by == "hour":
        select_query = """SELECT YEAR(check_in) AS year, MONTH(check_in) AS month, DAY(check_in) AS day, HOUR(check_in) AS hour, COUNT(*) AS n_cars 
                            FROM CarRecord GROUP BY year, month, day, hour ORDER BY year, month, day, hour ASC"""
    elif grouped_by == "day":
        select_query = """SELECT YEAR(check_in) AS year, MONTH(check_in) AS month, DAY(check_in) AS day, COUNT(*) AS n_cars 
                            FROM CarRecord GROUP BY year, month, day ORDER BY year, month, day ASC"""
    elif grouped_by == "month":
        select_query = """SELECT YEAR(check_in) AS year, MONTH(check_in) AS month, COUNT(*) AS n_cars 
                            FROM CarRecord GROUP BY year, month ORDER BY year, month ASC"""
    elif grouped_by == "year":
        select_query = """SELECT YEAR(check_in) AS year, COUNT(*) AS n_cars 
                            FROM CarRecord GROUP BY year ORDER BY year ASC"""

    cursor = connection_object.cursor(named_tuple=True)
    try:
        if select_query is not None:
            cursor.execute(select_query)
            rows = cursor.fetchall()
            data = {}
            for index, row in enumerate(rows):
                invoice = {}
                for j in [
                    {i[0]: str(i[1])} for i in list(row._asdict().items())
                ]:
                    invoice.update(j)
                data.update({index: invoice})
            response = {
                "message": "List of all the cars parked at the moment",
                "data": data,
            }
            return make_response(jsonify(response), 200)
        else:
            abort(404)
    except Error as err:
        print("Error Code:", err.errno)
        print("SQLSTATE:", err.sqlstate)
        print("Message:", err.msg)
    finally:
        cursor.close()
