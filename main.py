from flask import Flask, make_response,  request, jsonify
from flask_mysqldb import MySQL


app = Flask(__name__)

# MySQL configurations
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "202280287PSU"
app.config["MYSQL_DB"] = "kwikkwikcafe"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)  # Create an instance of MySQL and bind it to the Flask app


@app.route("/")
def hello_world():
    return "<p> hello ceianyy</p>"


@app.route("/branch", methods=["GET"])
def get_countries():
    cur = mysql.connection.cursor()
    query = "SELECT * FROM kwikkwikcafe.branch"
    cur.execute(query)
    data = cur.fetchall()
    cur.close()

    return make_response(jsonify(data), 200)


@app.route("/branch/<int:id>", methods=["GET"])
def get_branch_by_id(id):
    cur = mysql.connection.cursor()
    query = """
    SELECT * FROM branch where BranchID = {} """.format(id)
    cur.execute(query)
    data = cur.fetchall()
    cur.close()

    return make_response(jsonify(data), 200)


@app.route("/branch", methods=["POST"])
def add_branch():
    cur = mysql.connection.cursor()
    info = request.get_json()
    Branch_location = info["Branch_Location"]
    Branch_name = info['Branch_Name']
    sales = int(info['Total_Sales'])
    cur.execute("""
        INSERT INTO branch (Branch_Name, Branch_Location, Total_Sales)
        VALUES (%s, %s, %s)
        """, (Branch_name, Branch_location, sales))
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()

    return make_response(jsonify({"message": "Branch added sucessfully",
                                  "rows_affected": rows_affected}), 200)


@app.route("/branch/<int:id>", methods=["PUT"])
def update_actor(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    Branch_location = info["Branch_Location"]
    Branch_name = info['Branch_Name']
    cur.execute(
        """ UPDATE branch SET Branch_location = %s, Branch_Name = %s
        WHERE BranchID = %s """,
        (Branch_location, Branch_name, id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "actor updated successfully",
             "rows_affected": rows_affected}
        ),
        200,
    )


@app.route("/branch/<int:id>", methods=["DELETE"])
def delete_actor(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM branch where BranchID = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "actor deleted successfully",
             "rows_affected": rows_affected}
        ),
        200,
    )


if __name__ == "__main__":
    app.run(debug=True)
