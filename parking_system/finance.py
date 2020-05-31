from mysql.connector import MySQLConnection, Error
from flask import Blueprint, request, url_for, make_response, jsonify, abort
from calendar import month_name
from parking_system.db_dao import get_db

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
            abort(404)
    except Error as err:
        print("Error Code:", err.errno)
        print("SQLSTATE:", err.sqlstate)
        print("Message:", err.msg)
    finally:
        cursor.close()
