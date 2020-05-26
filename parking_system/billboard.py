from collections import namedtuple

from mysql.connector import MySQLConnection, Error
from flask import Blueprint, flash, render_template, request, url_for
from parking_system.db_dao import get_db


blueprint = Blueprint("billboard", __name__, url_prefix="/billboard")


@blueprint.route("/info", methods=(["GET"]))
def get_parking_spaces_info():
    """Gets information about the parking lots in terms of parking spaces

        Returns
        -------
        rows : list 
            List of named tuples containing strings of the columns data,
            representing the rows in the ParkingLot table of the MySQL database
            i.e.
            rows[n].name -> (str) name of the parking lot
            rows[n].non_charging -> (str) number of available/occupied non-charging spaces
            rows[n].charging -> (str) number of available/occupied charging spaces
        is_occupied_arg : str
            "0" or "1"
            specifies whether the returned data represents available or occupied spaces
    """

    is_occupied_field = request.args.get("is_occupied")
    if is_occupied_field is None:
        is_occupied_field = "0"
    connection_object = get_db("billboard")
    cursor = connection_object.cursor(named_tuple=True)
    select_query = """SELECT name,
                            COUNT(IF(space_type = 'non_charging', 1, NULL)) 'non_charging',
                            COUNT(IF(space_type = 'charging', 1, NULL)) 'charging'
                                FROM (
                                    SELECT pl.lot_id, pl.name, pl.location, pl.capacity_all, pl.capacity_charging, ps.space_id, ps.space_type, ps.is_occupied 
                                        FROM ParkingLot pl 
                                            INNER JOIN ParkingSpace ps 
                                                ON pl.lot_id = ps.lot_id) pl_ps
                                WHERE pl_ps.is_occupied = %s
                            GROUP BY name
                        """
    try:
        cursor.execute(select_query, (is_occupied_field,))
        rows = cursor.fetchall()
        if rows is None:
            flash("No recorded data")
        return render_template(
            "billboard/info.html",
            lots_info=rows,
            is_occupied_arg=is_occupied_field,
        )
    except Error as err:
        print("Error Code:", err.errno)
        print("SQLSTATE:", err.sqlstate)
        print("Message:", err.msg)
    finally:
        cursor.close()
