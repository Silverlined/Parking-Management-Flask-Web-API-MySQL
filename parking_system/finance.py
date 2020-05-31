from mysql.connector import MySQLConnection, Error
from flask import (
    Blueprint,
    url_for,
    request,
    url_for,
    make_response,
    jsonify,
    redirect,
    abort,
)
from calendar import month_name
from parking_system.db_dao import get_db
from parking_system import maintenance
from calendar import month_name

blueprint = Blueprint("finance", __name__, url_prefix="/api/v1/finance")


@blueprint.route("/list-cars", methods=(["GET"]))
def get_cars_date_range():
    start_date = request.args.get("start-date")
    end_date = request.args.get("end-date")
    connection_object = get_db("finance_app")
    select_query = """SELECT c.owner_id, c.license_plate, c.brand_name, c.fuel_type
                        FROM
                            Car c
                        INNER JOIN CarRecord r ON c.license_plate = r.license_plate AND r.check_in >= %s AND r.check_in <= %s"""

    cursor = connection_object.cursor(named_tuple=True)
    try:
        if start_date is not None and end_date is not None:
            cursor.execute(select_query, (start_date, end_date))
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
                "message": "List cars parked from %s until %s"
                % (start_date, end_date),
                "data": data,
            }
            return make_response(jsonify(response), 200)
        else:
            return redirect(url_for("maintenance.get_currently_parked_cars"))
    except Error as err:
        print("Error Code:", err.errno)
        print("SQLSTATE:", err.sqlstate)
        print("Message:", err.msg)
    finally:
        cursor.close()


@blueprint.route("/invoice/<email>/<month>")
def get_user_invoice(email, month):
    connection_object = get_db("finance_app")
    cursor = connection_object.cursor(named_tuple=True)
    ### Reverse month name to month index
    month_n = None
    for index, i in enumerate(list(month_name)):
        if str(i).lower() == str(month).lower():
            month_n = index
    if month_n is None:
        abort(404)
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
                                        INNER JOIN CarOwner ON Car.owner_id = CarOwner.owner_id AND CarOwner.email = %s
                                    ) co
                                INNER JOIN CarRecord r ON co.license_plate = r.license_plate AND MONTH(r.check_in) = %s
                                ) cor
                                INNER JOIN ParkingSpace ps USING(space_id)"""
    try:
        cursor.execute(select_query, (email, month_n))
        rows = cursor.fetchall()
        data = {}
        for index, row in enumerate(rows):
            invoice = {}
            for j in [{i[0]: str(i[1])} for i in list(row._asdict().items())]:
                invoice.update(j)
            data.update({index: invoice})
        response = {"message": "Monthly invoice of a car owner", "data": data}
        return make_response(jsonify(response), 200)
    except Error as err:
        print("Error Code:", err.errno)
        print("SQLSTATE:", err.sqlstate)
        print("Message:", err.msg)
    finally:
        cursor.close()


@blueprint.route("/unpaid", methods=(["GET"]))
def get_unpaid_records():
    connection_object = get_db("finance_app")
    cursor = connection_object.cursor(named_tuple=True)
    select_query = """SELECT * FROM CarRecord WHERE is_paid = 0"""

    try:
        cursor.execute(select_query)
        rows = cursor.fetchall()
        data = {}
        for index, row in enumerate(rows):
            invoice = {}
            for j in [{i[0]: str(i[1])} for i in list(row._asdict().items())]:
                invoice.update(j)
            data.update({index: invoice})
        response = {"message": "Monthly invoice of a car owner", "data": data}
        return make_response(jsonify(response), 200)
    except Error as err:
        print("Error Code:", err.errno)
        print("SQLSTATE:", err.sqlstate)
        print("Message:", err.msg)
    finally:
        cursor.close()
