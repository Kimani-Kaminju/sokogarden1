#import flask module
from flask import *
import pymysql
#pymysql-allows one to create a connection to the sql database

#create app
app = Flask(__name__)


#Define sign up/register url endpoint
@app.route("/api/signup",methods=["POST"])
def signup():
    if request.method =="POST":
        #get the details to pass from postman
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        phone= request.form["phone"]
        #create connection
        connection = pymysql.connect(host="localhost", password="", user="root",database="sokogarden")

        #create a cursor
        cursor = connection.cursor()

        #structure the sql query for insert
        # %s-pre-prepared statement.It is a placeholder that will replace actual value
        sql = "insert into users(username,password,email,phone) values (%s,%s,%s,%s)"

        #create a tuple to hold all your data available on the variables
        data = (username,password,email,phone)

        #by the use of the cursor,execute the sql query as you replace the placeholders with the actual value
        cursor.execute(sql,data)

        #commit/complete the changes to the database
        connection.commit()

        #give a response to the user
        return jsonify({"message" : "User registerd successfully"})



#Run
app.run(debug=True)