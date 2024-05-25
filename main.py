from flask import Flask, make_response, jsonify
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
    SELECT * FROM branch where branchID = {} """.format(id)
    cur.execute(query)
    data = cur.fetchall()
    cur.close()

    return make_response(jsonify(data), 200)


if __name__ == "__main__":
    app.run(debug=True)
