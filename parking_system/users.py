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
)
import re
import json
from uuid import UUID
from parking_system.db_dao import get_db
from parking_system.auth import login_required
from calendar import month_name


blueprint = Blueprint("users", __name__, url_prefix="/api/v1/users")


@blueprint.route("/register-car", methods=(["GET", "POST"]))
@login_required
def register_car():
    owner_id = g.user.owner_id
    if request.method == "POST":
        license_plate = request.form["license_plate"]
        brand_name = request.form["brand_name"]
        fuel_type = request.form["fuel_type"]
        connection_object = get_db("zernike_parking_app")
        error = None

        cursor = connection_object.cursor(named_tuple=True)
        duplication_check_query = """SELECT EXISTS(SELECT license_plate FROM Car WHERE license_plate =%s) AS isRegistered"""
        insert_query = """INSERT INTO Car (license_plate, owner_id, brand_name, fuel_type) VALUES (%s,%s,%s,%s)"""

        try:
            error = validate_car_data(license_plate, brand_name, fuel_type)
            cursor.execute(duplication_check_query, (license_plate,))
            if cursor.fetchone().isRegistered == 1:
                error = (
                    "Already registered car with this license plate (%s)."
                    % license_plate
                )
            if error is None:
                cursor.execute(
                    insert_query,
                    (license_plate, owner_id, brand_name, fuel_type),
                )
                connection_object.commit()
                response = {
                    "message": "Car registered",
                    "data": {
                        "owner_id": str(owner_id),
                        "license_plate": license_plate,
                        "brand_name": brand_name,
                        "fuel_type": fuel_type,
                    },
                }
                return make_response(jsonify(response), 201)
        except Error as err:
            connection_object.rollback()
            print("Error Code:", err.errno)
            print("SQLSTATE:", err.sqlstate)
            print("Message:", err.msg)
        finally:
            cursor.close()
            if error is not None:
                flash(error)

    return render_template("users/register_car.html")


@blueprint.route("/invoice", methods=(["GET"]))
@login_required
def get_invoice():
    owner_id = g.user.owner_id
    month = request.args.get("month")
    connection_object = get_db("zernike_parking_app")
    cursor = connection_object.cursor(named_tuple=True)
    select_query = """SELECT
                                license_plate,
                                check_in,
                                check_out,
                                total_time,
                                total_time * ps.hourly_tariff AS parking_cost,
                                is_paid
                            FROM
                                (
                                SELECT
                                    co.license_plate,
                                    r.check_in,
                                    r.check_out,
                                    ROUND(
                                        (
                                            TIME_TO_SEC(
                                                TIMEDIFF(r.check_out, r.check_in)
                                            ) / 3600
                                        ),
                                        2
                                    ) AS total_time,
                                    r.is_paid,
                                    r.space_id
                                FROM
                                    (
                                    SELECT
                                        Car.license_plate,
                                        CarOwner.owner_id,
                                        CarOwner.first_name,
                                        CarOwner.surname,
                                        CarOwner.student_employee_code,
                                        CarOwner.discount_rate,
                                        CarOwner.payment_method
                                    FROM
                                        Car
                                    INNER JOIN CarOwner ON Car.owner_id = CarOwner.owner_id AND CarOwner.owner_id = %s
                                ) co
                            INNER JOIN CarRecord r ON co.license_plate = r.license_plate AND MONTH(r.check_in) = %s
                            ) cor
                            INNER JOIN ParkingSpace ps USING(space_id)"""
    try:
        cursor.execute(select_query, (owner_id, month))
        rows = cursor.fetchall()
        data = [
            {
                "license_plate": row.license_plate,
                "check_in": row.check_in,
                "check_out": row.check_out,
                "total_time": str(row.total_time),
                "parking_cost": str(row.parking_cost),
            }
            for index, row in enumerate(rows)
        ]
        # for index, row in enumerate(data):
        # data.setdefault(index, []).append(row)
        # result.insert(
        #     index,
        #     [
        #         owner_id,
        #         row.license_plate,
        #         row.check_in,
        #         row.check_out,
        #         row.total_time,
        #         row.parking_cost,
        #     ],
        # )
        response = {
            "message": "User invoice for month %s"
            % month_name[int(month)],
            "data": data,
        }
        return make_response(jsonify(response), 201)
    except Error as err:
        print("Error Code:", err.errno)
        print("SQLSTATE:", err.sqlstate)
        print("Message:", err.msg)
    finally:
        cursor.close()


def validate_car_data(license_plate, brand_name, fuel_type):
    if not re.match(r"^[A-Z]{1,3}[A-Z]{1,2}[0-9]{1,4}$", license_plate):
        error = "Please Enter A Valid License Plate\ne.g. AAABB1234"
        return error

    if not re.match(r"[a-zA-Z\s]{0,20}$", brand_name):
        error = "Please enter car brand"
        return error

    if not re.match(r"[a-zA-Z\s]{0,10}$", fuel_type):
        error = "Please enter car fuel type"
        return error

    return None
