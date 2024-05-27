from flask import Flask, request, jsonify, make_response, render_template
from flask_mysqldb import MySQL
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "202280287PSU"
app.config["MYSQL_DB"] = "kwikkwikcafe"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)
auth = HTTPBasicAuth()

# Create a simple user storage
users = {
    "Bryan": generate_password_hash("root"),
    "Alice": generate_password_hash("wonderland")
}


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username),
                                                 password):
        return username
    return None


@app.route('/')
def hello_world():
    return "<p>Welcome</p>"


def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data


@app.route('/public')
def public():
    return 'For Public'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')

        if verify_password(username, password):
            return jsonify({'message': 'Login successful'})
        else:
            return make_response('Unable to verify', 403,
                                 {'WWW-Authenticate':
                                     'Basic realm: "Authentication Failed "'})
            
    else:
        return render_template('login.html')


@app.route("/branch", methods=["GET"])
@auth.login_required
def get_countries():
    cur = mysql.connection.cursor()
    query = "SELECT * FROM kwikkwikcafe.branch"
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return make_response(jsonify(data), 200)


@app.route("/branch/<int:id>", methods=["GET"])
@auth.login_required
def get_branch_by_id(id):
    cur = mysql.connection.cursor()
    query = "SELECT * FROM branch WHERE BranchID = %s"
    cur.execute(query, (id,))
    data = cur.fetchall()
    cur.close()
    return make_response(jsonify(data), 200)


@app.route("/branch", methods=["POST"])
@auth.login_required
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
    rows_affected = cur.rowcount
    cur.close()
    return make_response(jsonify({"message": "Branch added successfully",
                                  "rows_affected": rows_affected}), 200)


@app.route("/branch/<int:id>", methods=["PUT"])
@auth.login_required
def update_branch(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    Branch_location = info["Branch_Location"]
    Branch_name = info['Branch_Name']
    cur.execute("""
        UPDATE branch SET Branch_Location = %s, Branch_Name = %s
        WHERE BranchID = %s
    """, (Branch_location, Branch_name, id))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(jsonify({"message": "Branch updated successfully",
                                  "rows_affected": rows_affected}), 200)


@app.route("/branch/<int:id>", methods=["DELETE"])
@auth.login_required
def delete_branch(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM branch WHERE BranchID = %s", (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(jsonify({"message": "Branch deleted successfully",
                                  "rows_affected": rows_affected}), 200)


if __name__ == "__main__":
    app.run(debug=True)
