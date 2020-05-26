import functools
from collections import namedtuple
from uuid import uuid1, UUID
from mysql.connector import MySQLConnection, Error
from passlib.hash import sha256_crypt
import re
from parking_system.db_dao import get_db
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@blueprint.route("/register", methods=(["GET", "POST"]))
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        customer_type = request.form["customer_type"]
        student_employee_code = request.form["student_employee_code"]
        first_name = request.form["first_name"]
        surname = request.form["surname"]
        tel_number = request.form["tel_number"]
        payment_method = request.form["payment_method"]
        connection_object = get_db("zernike_parking_app")
        error = None

        cursor = connection_object.cursor(named_tuple=True)
        duplication_check_query = """SELECT EXISTS(SELECT email FROM CarOwner WHERE email=%s) AS is_registered"""
        insert_query = """INSERT INTO CarOwner (owner_id, customer_type, student_employee_code, first_name, surname, tel_number, email, password, payment_method) 
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        try:
            error = validate_user_data(
                email,
                password,
                student_employee_code,
                first_name,
                surname,
                tel_number,
            )
            cursor.execute(duplication_check_query, (email,))
            if cursor.fetchone().is_registered == 1:
                error = "Already registered email address (%s)." % email

            if error is None:
                cursor.execute(
                    insert_query,
                    (
                        uuid1().bytes,
                        customer_type,
                        student_employee_code,
                        first_name,
                        surname,
                        tel_number,
                        email,
                        sha256_crypt.hash(password),
                        payment_method,
                    ),
                )
                connection_object.commit()
                return redirect(url_for("billboard.info"))

        except Error as err:
            connection_object.rollback()
            print("Error Code:", err.errno)
            print("SQLSTATE:", err.sqlstate)
            print("Message:", err.msg)
        finally:
            cursor.close()
            if error is not None:
                flash(error)

    return render_template("auth/register.html")


@blueprint.route("/register-car", methods=(["GET", "POST"]))
def register_car():
    # if g.user is None:
    #     return redirect(url_for("auth.login"))
    if request.method == "POST":
        owner_id = g.user.owner_id

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


@blueprint.route("/login", methods=(["GET", "POST"]))
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        connection_object = get_db("zernike_parking_app")
        error = None
        user = None
        verify_email_query = """SELECT EXISTS(SELECT email FROM CarOwner WHERE email=%s) AS is_registered"""
        get_pass_hash_query = """SELECT password FROM CarOwner WHERE email=%s"""

        cursor = connection_object.cursor(named_tuple=True)
        try:
            cursor.execute(verify_email_query, (email,))
            email_is_registered = cursor.fetchone().is_registered
            cursor.execute(get_pass_hash_query, (email,))
            password_hash = cursor.fetchone().password
            if email_is_registered == 0:
                error = "Incorrect email address."
            elif not sha256_crypt.verify(password, password_hash):
                error = "Incorrect password."

            if error is None:
                cursor.execute(
                    "SELECT * FROM CarOwner WHERE email=%s ", (email,)
                )
                user = cursor.fetchone()
                session.clear()
                session["user_id"] = UUID(bytes=user.owner_id)
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
    return render_template("auth/login.html")


# TODO: Fix UUID check
@blueprint.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    print(user_id)
    if user_id is None:
        g.user = None
    else:
        try:
            cursor = get_db("zernike_parking_app").cursor(named_tuple=True)
            cursor.execute(
                "SELECT * FROM CarOwner WHERE owner_id=UUID_TO_BIN(%s) ",
                (user_id,),
            )
            g.user = cursor.fetchone()
        except Error as err:
            print("Error Code:", err.errno)
            print("SQLSTATE:", err.sqlstate)
            print("Message:", err.msg)
        finally:
            cursor.close()


@blueprint.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view


def validate_user_data(
    email, password, student_employee_code, first_name, surname, tel_number
):
    if not re.match(r"^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$", email):
        error = "Invalid email address"
        return error
    elif re.match(r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.{8,42})$", password):
        error = "Password required.\nMinimum length - 8 characters."
        return error
    if not re.match(r"^$|^[0-9]{6}$", student_employee_code):
        error = "Please Enter Your Student/Employee Code\n(6 digit number)"
        return error

    if not re.match(r"[a-zA-Z\s]{0,20}$", first_name):
        error = "Please Enter Your First Name"
        return error

    if not re.match(r"[a-zA-Z\s]{0,20}$", surname):
        error = "Please Enter Your Surname"
        return error

    if not re.match(
        r"^$|^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$", tel_number
    ):
        error = "Please Enter Your Tel. Number"
        return error
    return None


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
