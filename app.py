#import flask module
from flask import *
import pymysql
#pymysql-allows one to create a connection to the sql database

import os

#create app
app = Flask(__name__)
#below we configure where product image shall be saved
app.config["UPLOAD_FOLDER"] = 'static/images'

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

        # Check if email already exists
        check_sql = "SELECT * FROM users WHERE email = %s"
        cursor.execute(check_sql, (email,))
        user = cursor.fetchone()
        if user:
            return jsonify({"message": "user already registered"})

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
        return jsonify({"message" : "User registered successfully"})
#import pymysql cursor
import pymysql.cursors
#below is the sign in api end point
@app.route("/api/signin",methods=["POST"])  
def signin():
    if request.method == "POST":
        #extract the dta from post man
        email = request.form["email"]
        password = request.form["password"]

        #create a connection to db
        connection = pymysql.connect(host="localhost",password="",user="root",database="sokogarden")

        #create cursor
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        #structure the sql query to check whether the person trying to login already has an account
        sql = "select * from users where email = %s and password = %s"

        #tuple
        data = (email , password)
        #cursor,execute the query
        cursor.execute(sql,data)

        #check how many rows are returned when the query is executed
        count = cursor.rowcount

        if count == 0:
            return jsonify({"message": "Login failed.Please check on your details entered"})   
        else:
            #if the user is there, take the details of the user and store them onto a variable and return a message of success
            user = cursor.fetchone()
            return jsonify({"message" : "Login success" , "user": user})


#Define url endpoint
@app.route("/api/addproduct",methods = ["POST"])
def products():
    if request.method == "POST":
        #details to pass from postman
        product_name = request.form["product_name"]
        product_description = request.form["product_description"]
        product_cost = request.form["product_cost"]
        product_photo = request.files["product_photo"]
        product_category = request.form["product_category"]
        
        #since the product is a type of a file we shall extract the name of the product and that name shall be stored into the database whill the photo of the product shall be stored into the static/images folder

        filename = product_photo.filename

        #specify where the image will be saved
        
        photo_path = os.path.join(app.config["UPLOAD_FOLDER"],filename)

        #save the image
        product_photo.save(photo_path)
        #create a connection of the db to the postman
        connection = pymysql.connect(host="localhost",password="",user="root",database="sokogarden")

        #create cursor
        cursor = connection.cursor()

        #sql structure for insert
        sql = "INSERT INTO product_details( product_name,product_description,product_cost,product_photo,product_category) values (%s,%s,%s,%s,%s)"

        
        #create a tuple to hold the data
        data = (product_name, product_description, product_cost, filename, product_category)

        #use cursor to execute the sql query
        cursor.execute(sql,data)

        #commit the changes to the database
        connection.commit()

       #response to user
        return jsonify({"message" : "Product added Successfully"}) 
    
#below is the get product route
@app.route("/api/getproducts",methods=["GET"])
def get_product_method():
    if request.method == "GET":

        #create connection to db
        connection = pymysql.connect(host="localhost",user="root",password="",database="sokogarden")

        #below is our cursor
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        #SQL query for fetching all products
        sql = "select * from product_details"

        #execute the cursor
        cursor.execute(sql)

        #create a variable that will hold all those products
        products = cursor.fetchall()
        
        #close the connection
        connection.close()

        #return the products as the response 
        return jsonify(products)



#Run
app.run(debug=True)