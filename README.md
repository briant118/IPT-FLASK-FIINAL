KwikKwik Cafe API

Overview

KwikKwik Cafe API is a simple Flask-based application for managing branches of a cafe. It includes user authentication, and CRUD operations for branch data stored in a MySQL database.

Features
  User authentication using sessions.
  CRUD operations for branches:
  Retrieve all branches.
  Retrieve a branch by ID.
  Add a new branch.
  Update an existing branch.
  Delete a branch.
  
Requirements
  Python 3.x
  MySQL database

Installation
  1. clonne repository: https://github.com/briant118/IPT-FLASK-FIINAL.git
  2. Set up a virtual environment: python3 -m venv privatefile then activate source privatefile/Scripts/activate
  3. Install the required libraries pip install -r requirements.txt
  4. Set up MySQL database
    Install MySQL and create a database named kwikkwikcafe.
    Create a table named branch with the following structure:

    CREATE TABLE branch (
    BranchID INT AUTO_INCREMENT PRIMARY KEY,
    Branch_Name VARCHAR(100),
    Branch_Location VARCHAR(100),
    Total_Sales INT
      );
  6. Create a MySQL user with appropriate permissions and update the database configuration in main.py
     app.config["MYSQL_HOST"] = "localhost"
     app.config["MYSQL_USER"] = "your_mysql_user"
     app.config["MYSQL_PASSWORD"] = "your_mysql_password"
     app.config["MYSQL_DB"] = "kwikkwikcafe"
     app.config["MYSQL_CURSORCLASS"] = "DictCursor"

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.
  


  
  


