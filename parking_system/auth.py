import functools
from uuid import uuid1
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
    """Registers a new car owner in the database

        GET:
            responses:
                200 OK on success,
                404 Not Found
        POST:
            parameters:
                email: str
                password: str
                customer_type: str
                student_employee_code: str
                first_name: str
                surname: str
                tel_number: str
                payment_method: str
            responses:
                201 Created on success
    """

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
                return redirect(url_for("billboard.info"), code=201)
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


@blueprint.route("/login", methods=(["GET", "POST"]))
def login():
    """Login as a car owner

        GET:
            responses:
                200 OK on success,
                404 Not Found
        POST:
            parameters:
                email: str
                password: str
            responses:
                204 No Content on success
    """

    if request.method == "POST":
        email = request.form["email"]
        print(email)
        password = request.form["password"]
        connection_object = get_db("zernike_parking_app")
        error = None
        verify_email_query = """SELECT EXISTS(SELECT email FROM CarOwner WHERE email=%s) AS is_registered"""
        get_pass_hash_query = """SELECT password FROM CarOwner WHERE email=%s"""

        cursor = connection_object.cursor(named_tuple=True)
        try:
            cursor.execute(verify_email_query, (email,))
            email_is_registered = cursor.fetchone().is_registered

            if email_is_registered == 0:
                error = "Incorrect email address."
            else:
                cursor.execute(get_pass_hash_query, (email,))
                password_hash = cursor.fetchone().password
                if not sha256_crypt.verify(password, password_hash):
                    error = "Incorrect password."

            if error is None:
                cursor.execute(
                    "SELECT BIN_TO_UUID(owner_id) AS owner_id FROM CarOwner WHERE email=%s ",
                    (email,),
                )
                user_id = cursor.fetchone().owner_id
                session.clear()
                session["user_id"] = user_id
                return redirect(
                    url_for("billboard.get_parking_spaces_info"), code=204
                )

        except Error as err:
            connection_object.rollback()
            print("Error Code:", err.errno)
            print("SQLSTATE:", err.sqlstate)
            print("Message:", err.msg)
        except ValueError as err:
            print("login failure: ", err)
        finally:
            cursor.close()
            if error is not None:
                flash(error)
    return render_template("auth/login.html")


@blueprint.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        try:
            cursor = get_db("zernike_parking_app").cursor(named_tuple=True)
            cursor.execute(
                "SELECT * FROM CarOwner WHERE owner_id=UUID_TO_BIN(%s) LIMIT 1",
                (user_id,),
            )
            g.user = cursor.fetchone()
        except Error as err:
            print("Error Code:", err.errno)
            print("SQLSTATE:", err.sqlstate)
            print("Message:", err.msg)
        finally:
            cursor.close()


@blueprint.route("/logout", methods=(["GET"]))
def logout():
    # session.clear()
    [session.pop(key) for key in list(session.keys()) if key != "_flashes"]
    flash("Successfully logged out.", "info")
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
