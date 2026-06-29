#import all from flask
from flask import *

#import pymysql
import pymysql

#Create app
app = Flask(__name__)

#Define url endpoint
@app.route("/api/products",methods = ["POST"])
def products():
    if request.method == "POST":
        #details to pass from postman
        product_name = request.form["product_name"]
        product_description = request.form["product_description"]
        product_cost = request.form["product_cost"]
        product_photo = request.form["product_photo"]
        product_category = request.form["product_category"]

        #create a connection of the db to the postman
        connection = pymysql.connect(host="localhost",password="",user="root",database="sokogarden")

        #create cursor
        cursor = connection.cursor()

        #sql structure for insert
        sql = "insert to products( product_name, product_description, product_cost, product_photo, product_category)"
        
        #create a tuple to hold the data
        data = (product_name, product_description, product_cost, product_photo, product_category)

        #use cursor to execute the sql query
        cursor.execute(sql,data)

        #commit the changes to the database
        connection.commit

       #response to user
    return jsonify({"message" : "Product entered"}) 
