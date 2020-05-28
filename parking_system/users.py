from mysql.connector import MySQLConnection, Error
from flask import (
    Blueprint,
    flash,
    render_template,
    request,
    url_for,
    g,
    redirect,
)
import re
from parking_system.db_dao import get_db
from parking_system.auth import login_required


blueprint = Blueprint("users", __name__, url_prefix="/users")


@blueprint.route("/register-car", methods=(["GET", "POST"]))
def register_car():
    if g.user is None:
        owner_id = None
    else:
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
                return redirect(url_for("billboard.get_parking_spaces_info"))

        except Error as err:
            connection_object.rollback()
            print("Error Code:", err.errno)
            print("SQLSTATE:", err.sqlstate)
            print("Message:", err.msg)
        finally:
            cursor.close()
            if error is not None:
                flash(error)

    return render_template("auth/register_car.html")


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
