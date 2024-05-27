from flask import Flask, request, jsonify, make_response, render_template, session, redirect, url_for
from flask_mysqldb import MySQL
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import functools

app = Flask(__name__)

# Configurations
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


def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')

        if verify_password(username, password):
            session['username'] = username
            return jsonify({'message': 'Login successful'})
        else:
            return make_response('Unable to verify', 403,
                                 {'WWW-Authenticate':
                                     'Basic realm: "Authentication Failed "'})

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


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


@app.route("/branch", methods=["GET"])
@login_required
def get_branches():
    cur = mysql.connection.cursor()
    query = "SELECT * FROM kwikkwikcafe.branch"
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return make_response(jsonify(data), 200)


@app.route("/branch/<int:id>", methods=["GET"])
@login_required
def get_branch_by_id(id):
    cur = mysql.connection.cursor()
    query = "SELECT * FROM branch WHERE BranchID = %s"
    cur.execute(query, (id,))
    data = cur.fetchall()
    cur.close()
    return make_response(jsonify(data), 200)


@app.route("/branch", methods=["POST"])
@login_required
def add_branch():
    info = request.get_json()
    Branch_location = info["Branch_Location"]
    Branch_name = info['Branch_Name']
    sales = int(info['Total_Sales'])

    cur = mysql.connection.cursor()
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
@login_required
def update_branch(id):
    info = request.get_json()
    Branch_location = info["Branch_Location"]
    Branch_name = info['Branch_Name']

    cur = mysql.connection.cursor()
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
@login_required
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
