#import flask and its components
from flask import *
import os

#import the pymysql module- It helps us to create a connection between python flask and mysql database
import pymysql

# Create a flask application and give it a name 
app = Flask(__name__)

# configure te location to where your product images will be saved on your application
app.config["UPLOAD_FOLDER"] = "static/images"


# below is the sign up route
@app.route("/api/signup", methods = ["POST"])
def signup():
    if request.method== "POST":
        # extract the different details entered on the form 
        username = request.form["username"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]

        # by use of the print function lets print all those details sent with the upcoming request
        # print(username, email, password, phone)

        #establish a connection between flask/python and mysql
        connection = pymysql.connect(host="localhost", user="root", password="",database="sokogardenonline")

        #create a cursor to execute the sql queries
        cursor = connection.cursor()
        
        # structure an sql to insert the details received  from the form

        #The %s is a placeholder -> A PLACEHOLDER IT STANDS IN PLACES OF ACTUAL VALUES
        sql = "INSERT INTO user(username, email, phone, password) VALUES(%s, %s, %s, %s)"

        #create a tuple that will hold all the data gotten from the form
        data = (username, email, phone, password)

        #by use of the cursor execute the sql as you replace the placeholders with actual values
        cursor.execute(sql, data)

        #commit the changes to the database 
        connection.commit()
        return jsonify ({"message":"User registered successfully."})





# Below is the login/signup route
@app.route("/api/signin", methods=["POST"])
def signin():
    if request.method == "POST":
        # extract the two details entered in the form
        email = request.form ["email"]
        password = request.form ["password"] 

        # print out the details entered
        # print(email, password)

        # create/ establish a connection to the database
        connection = pymysql.connect(host="localhost", user="root", password="" , database= "sokogardenonline")

        #create a cursor
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        # structure the sql query that will check whether the email and password entered are correct
        sql = "SELECT * FROM user WHERE email = %s AND password = %s"

        #put the data received from the form into a tuple
        data = (email, password)

        # by use of the cursor execute the sql
        cursor.execute(sql, data)

        #check whether there are rows returned and the store on the variable
        count=cursor.rowcount

        # if there are records returned it means the password and the email are correct otherwise it means the are wrong
        if count == 0:
            return jsonify({"message": "login failed"})
        else:
            # there must be a user so we create a variable that will hold the details of the user fetched from the database
            user= cursor.fetchone()
            #return the details to the frontend as well as a message
            return jsonify({"message": "user logged in successfully","user":user})



#Below is the route of adding products
@app.route("/api/add_product", methods = ["POST"])
def Addproducts():
    if request.method == "POST":
        
        #extract the data eneterd on the form
        product_name = request.form["product_name"]
        product_description = request.form["product_description"]
        product_cost = request.form["product_cost"]
        # for the product_photo, we shall fetch it from the files
        product_photo = request.files["product_photo"]

        # extract the filename of the product photo
        filename = product_photo.filename
        #by use of the os module (operating system) we can extract the file path where the image is currently saved
        photo_path= os.path.join(app.config["UPLOAD_FOLDER"], filename)
        #save the product_photo image into the new location
        product_photo.save(photo_path)

        #print them out to test whether you are receiving the details sent with the request
        # print(product_name, product_description, product_cost, product_photo)
        

        connection = pymysql.connect(host="localhost", user= "root", password="", database="sokogardenonline")

        #create connection using cursor
        cursor = connection.cursor()

        sql = "INSERT INTO product_details(product_name, product_description, product_cost, product_photo) VALUES(%s, %s, %s, %s)"

        #create a tuple that will hold the data from which are current held onto the diferent variable declared
        data = (product_name, product_description, product_cost, filename)

        #use the cursor to execute the sql as you replace the placeholders with actual data.
        cursor.execute(sql, data)

        #commit the changes to the database
        connection.commit()














        return jsonify ({"message": "Add product added accessed"})
        








        







#run the application
app.run(debug=True)