from flask import Flask, render_template, request, url_for
import sqlite3 as sql
import random
import string
from datetime import datetime
import boto3
from werkzeug.utils import secure_filename
import s3_bucket_operations
import bucket_names_object
import contains_all_urls_for_s3_buckets
from user_login_obj import user_login_obj
from product_info_obj import product_info_obj
import dynamoDB


"""
Importing serveral packages
- Flask
    - Flask
    - render_template
    - request
- sqlite
- random
- string
- datetime
- boto3
- secure_filename
Using  a user database and flask, creates a program to add users with several bits of info such as:
user_id, enail, first and last name, password and address details
Checks to see if the email already exists in the database.
Allows user to list all users for debugging purposes
Includes login function where the the user and upload picture to an S3 bucket to be resized
New product database. Allows user to add new products (checks to see if the  has already been added)
and then saves to database. User can also list all products in the database.
"""

app = Flask(__name__, template_folder='templates')  # Sets the templates folder for the website
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024  # Sets maximum filesize to be uploaded at 1MB

s3 = boto3.client('s3')  # Sets up S3 client
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}  # Only allowed extensions allowed for file upload
BUCKET_NAME = 'source-image-bucket-5623'

# global LOGIN # Global login variable

# START - Instantiate objects
hasAllBucketNamesObject = bucket_names_object.bucket_names_object()
containsAllUrlsForEachS3Bucket = contains_all_urls_for_s3_buckets.contains_all_urls_for_s3_buckets(
    hasAllBucketNamesObject)


# END - Instantiate objects

# Function checks if the email inputted from the user is currently in the database.
# Queries the user database by selecting emails where the saved email is the same as the user
# input email. Returns True is user is new or False if already registered user.
def IsUserNew(email):
    con = sql.connect("UserDatabase.db")  # The database to connect to
    cur = con.cursor()
    cur.execute("Select email from Users WHERE email=?", (email,))  # Queries database
    all_emails = cur.fetchall();  # Fetches output from query
    if len(all_emails) != 0:
        # Checks if the output of query is not 0. If it's not 0 that means the query has found a match
        # and therefore the email has been used already, i.e. exisiting user.
        return False
    return True


# Home page for website
# Returns the home.html template which allows the user to use the functions in the website.
@app.route('/')
def home():
    
    rows = dynamoDB.inventory_returnAllRecordData()

    return render_template('futureHomePage.html', rows=rows)


@app.route('/oldhome')
def oldHome():
    # print(user_role)
    # print(LOGIN)
    LOGIN = user.GetLogin()
    user_role = user.GetRole()
    if (LOGIN) and (user_role == "Warehouse" or user_role =="Authenticator"):
        return render_template('home.html')
    elif not LOGIN:
        msg = "Please login first"
        return render_template("new_result.html", msg=msg)
    else:
        msg = "Not authorised"
        return render_template("new_result.html", msg=msg)


# Called when the user wants to add a new user
# Returns the newuser.html template with the iput form required for getting the data from the user.
# Includes a role for who they are, depending on the role, they can use different functions.
@app.route('/enternewuserold')
def new_user():

    LOGIN = user.GetLogin()
    user_role = user.GetRole()

    if (LOGIN) and (user_role == "Warehouse" or "Authenticator"):
        roles = ['Warehouse', 'Authenticator', 'Customer']
        return render_template("newuser.html", roles=roles)
    elif not LOGIN:
        msg = "Please login first"
        return render_template("new_result.html", msg=msg)
    else:
        msg = "Not authorised"
        return render_template("new_result.html", msg=msg)

# newuser.html routes the form to this function
# Organises the data inputted from user for inserting to user database
@app.route('/adduser', methods=['POST', 'GET'])
def add_user():
    if request.method == "POST":
        try:
            # Creates user_id using random characters
            user_id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)])
            # Fetches information from html form
            email = request.form['email']
            fn = request.form['fn']
            ln = request.form['ln']
            pword = request.form['pword']
            addr = request.form['addr']
            city = request.form['city']
            role = request.form['role']

            # Checks if the user is new
            checkIfUserIsNew = IsUserNew(email)
            date_joined = str(datetime.now())
            if checkIfUserIsNew:  # If user is new then will add user details to database
                msg = dynamoDB.InsertNewUsers(user_id, email, fn, ln, pword, date_joined, addr, city, role)
            # This executes if user is not new
            if not checkIfUserIsNew:
                msg = "This is an exsiting user"
        except:
            con.rollback()
            msg = "Error in insert operation"

        finally:
            # Outputs the result of the operation
            # 1 of 3 options: Successfully add, not added due to existing user or error
            # Correct message will display depending on which of the 3 options happens
            return render_template("new_result.html", msg=msg)
            con.close()


# Lists the users in the database
# For debugging, will not be in the final website
@app.route('/list')
def list_users():
    con = sql.connect("UserDatabase.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from Users")

    rows = cur.fetchall();
    return render_template("list.html", rows=rows)


# USer login page, calls the check_user_login function
@app.route('/UserLogin')
def user_login():
    IsLoggedIn = user.GetLogin()

    if IsLoggedIn:
        msg = "You're already logged in."
        return render_template("new_result.html", msg=msg)

    return render_template('UserLogin.html')


# Checks if the users details entered are correct. If the email and password match for the same user then they are logged in succesfully
@app.route('/login', methods=['POST'])
def check_user_login():
    # global LOGIN, user_role, login_email

    LOGIN = user.GetLogin()
    user_role = user.GetRole()
    login_email = user.GetEmail()

    if request.method == "POST":
        try:
            # Gets the information from the user
            email = request.form['email']
            pword = request.form['pword']
            with sql.connect("UserDatabase.db") as con:
                cur = con.cursor()
                # Selects the user where email and password match
                cur.execute("Select * from Users WHERE email=? AND pword=?", (email, pword,))
                user_info = cur.fetchall();
                # If len(user_info) = 1, this means the query has found a user and therefore the user is logged in
                if len(user_info) == 1:
                    # User is told they are logged in
                    msg = "Successful Login"
                    # login_email = email
                    user.SetEmail(email)
                    # Sets the global variable, therefore allowing this to be seen later on
                    LOGIN = True
                    user.SetLogin(LOGIN)
                    cur.execute("Select role from Users WHERE email=? AND pword=?", (email, pword,))
                    user_role = cur.fetchall();
                    user_role = ''.join(user_role[0])
                    user.SetRole(user_role)
                    msg = "Successful Login and role is: " + user_role
                else:
                    # If anything else is found then the login is unsucessful and so the user is told
                    msg = "Unsuccessful Login"
                    LOGIN = False
                    user.SetLogin(LOGIN)
        except:
            con.rollback()
            msg = "Error in insert operation"

        finally:
            return render_template("new_result.html", msg=msg)
            con.close()

# For adding new products to inventory
@app.route('/newproduct')
def new_product():
    IsLoggedIn = user.GetLogin()
    usersRole = user.GetRole()
    
    if IsLoggedIn:
        if usersRole == 'Warehouse' or usersRole == 'Authenticator':

            # For the drop down menu if the item is authenticated or not
            authenticated = ['Yes', 'No']
            return render_template("newproduct.html", authenticated=authenticated)
        elif usersRole == 'Customer':

            msg = "You do not have permissions to access this page."
        
        else:
            msg = "This message should not be displayed. Something went wrong somewhere. This message is printed from WebAppForUsers.py in the function new_product()"
        
    else:

        msg = "You're not logged in, please log in first."
        
    return render_template("new_result.html", msg=msg)

# Using the product id, the product is checked to see if it already exists
def IsProdNew(prod_id):
    con = sql.connect("InventoryDatabase.db")  # Connects to the inventory Database
    cur = con.cursor()
    cur.execute("Select prod_id from Inventory WHERE prod_id=?",
                (prod_id,))  # Selects the products that have the same ID as the one given
    all_prod_id = cur.fetchall();
    if len(all_prod_id) != 0:  # If there are some clashes the new product is not added
        return False
    return True


def upload(prod_id, img):  # Uses the prod_id to name the picture uploaded to source bucket
    print("Inside upload function")    
    if img:
        print("Img is true")   
        filename = secure_filename(img.filename)  # Gets the file name for the picture
        fileNameSplit = filename.split(".")  # Splits the filename to get the extension
        fileExtention = fileNameSplit[1]
        print(filename)
        if fileExtention in ALLOWED_EXTENSIONS:  # Checks if the extensions are in the allowed extensions
            filename = prod_id + "." + fileExtention
            img.save(filename)
            # Uploads the file to the s3 bucket
            s3.upload_file(
                Bucket=(hasAllBucketNamesObject.getSourceBucketName),
                Filename=filename,
                Key=filename
            )
            msg = "Upload Done ! "  # Tells the user the upload is complete
        else:
            msg = "Not a png/jpg/jpeg."  # Error occurs if the extension is not an allowed extension and tells the user this

    return msg, filename


# Gets the information for the new product from the user via form
@app.route('/addproduct', methods=['POST', 'GET'])
def add_product():
    # global prod_id

    if request.method == "POST":
        try:

            prod_id = request.form['prod_ID']
            prod_name = request.form['prod_name']
            price = request.form['price']
            desc = request.form['desc']
            quantity = request.form['quantity']
            auth = request.form['auth']
            img = request.files['file']  # Takes the file, in this case apicture

            checkIfProdIsNew = IsProdNew(prod_id)  # Checks if the product is new or exisiting

            print("-------------> ") #Debug
            print(checkIfProdIsNew)

            if checkIfProdIsNew:
                print("In first If ")
                msgFromS3Upload, filename = upload(prod_id, img)
                print("-----yoyoyooy------")
                print(filename)
                temp_url = s3_bucket_operations.getUrlForOneProd(filename)
                msg = dynamoDB.InsertNewProducts(prod_id, prod_name, price, desc, quantity, auth, temp_url)
                msg = "Product successfully added"  # Tells the user the outcome
                msg = msg + " and " + msgFromS3Upload
            if not checkIfProdIsNew:  # If the product id is already there, the user will be told and the product is not added
                msg = "This is an exsiting product"
        except:
            con.rollback()
            msg = "Error in insert operation"

        finally:

            return render_template("new_result.html", msg=msg)
            con.close()


# List the products from the database for the users to see
@app.route('/listprods')
def list_prods():
    con = sql.connect("InventoryDatabase.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from Inventory")

    rows = cur.fetchall();
    print(rows)
    return render_template("listprods.html", rows=rows)


@app.route('/devTest')
# Show future version of what our home page will be
def devTest():
    # START - Dev test stuff
    # s3_bucket_operations.getFileNamesOfObjectsWithinAnS3Bucket(nameOfS3BucketToBeCalled = "refactored-image-bucket-5623")

    # s3_bucket_operations.getURLsOfAnObjectWithinAnS3Bucket(nameOfS3BucketToBeCalled="source-image-bucket-5623",
    #                                                        nameOfObjectFile="beach.jpg")

    print(s3_bucket_operations.getAllObjectsURLsFromS3AsList(nameOfS3BucketToBeCalled="refactored-image-bucket-5623"))

    # DATABASE STUFFS
    dbConnection = sql.connect("InventoryDatabase.db")
    dbConnection.row_factory = sql.Row

    cursor = dbConnection.cursor()
    # cursor.execute("select prod_url from Inventory")
    cursor.execute("select * from Inventory")

    rows = cursor.fetchall()

    print("\n -------- Database stuff from DEVTEST function ----------")
    print(rows)

    # END - Dev test stuff

    return render_template('futureHomePage.html', rows=rows)  # todo keep this here


@app.route('/dispImage')
def disp_image():
    return render_template('displayImage.html')

@app.route('/enternewuser')
def newRegistrationPage():
    IsLoggedIn = user.GetLogin()

    if IsLoggedIn:
         msg = "You are already logged in."
         return render_template("new_result.html", msg=msg)

    roles = ['Warehouse', 'Authenticator', 'Customer']
    return render_template('NewRegistrationPage.html', roles=roles)


@app.route('/userinfo')
def check_user_info():
    LOGIN = user.GetLogin()
    login_email = user.GetEmail()
    print(login_email)
    if LOGIN:
        # with sql.connect("UserDatabase.db") as con:
        #     cur = con.cursor()
        #     # Selects the user where email and password match
        #     cur.execute("Select * from Users WHERE email=?", (login_email,))
        #     user_info = cur.fetchall();
        #     print(user_info)

        # tup=user_info[0]

        # email = tup[1]
        # fn = tup[2]
        # ln = tup[3]
        # pword = tup[4]
        # date_joined = tup[5]
        # addr = tup[6]
        # city = tup[7]
        # role = tup[8]

        allItems = dynamoDB.users_returnAllRecordData()

        print(allItems)

        for record in allItems:
            # print(record['email'])
            if record['email'] == login_email:
                email = record['email']
                fn = record['first_name']
                ln = record['last_name']
                pword = record['pword']
                date_joined = record['date_joined']
                addr = record['address']
                city = record['city']
                role = record['role']
                break

        return render_template("UserInfo.html", email=email,fn=fn,ln=ln,pword=pword,date_joined=date_joined,addr=addr,city=city,role=role)
    else:
        msg = "Please login first"
        return render_template("new_result.html", msg=msg)

@app.route('/edituserinfo', methods=['POST', 'GET'])
def edit_user():
    # Fetches information from html form
    fn = request.form['fn']
    ln = request.form['ln']
    pword = request.form['pword']
    addr = request.form['addr']
    city = request.form['city']
    with sql.connect("UserDatabase.db") as con:
        cur = con.cursor()
        sql_query = """Update Users set first_name=?,last_name=?,pword=?,address=?,city=? where email=?"""
        data = (fn,ln,pword,addr,city,login_email)
        cur.execute(sql_query, data)
        con.commit()
        msg = "Record successfully edited"
    return render_template("new_result.html", msg=msg)

@app.route('/edituser')
def dispEditInfo():
    LOGIN = user.GetLogin()
    if LOGIN:
        return render_template('EditProfilePage.html')
    else:
        msg = "Please login first"
        return render_template("new_result.html", msg=msg)

@app.route('/deleteuser')
def delete_user():
    LOGIN = user.GetLogin()
    email = user.GetEmail()
    if LOGIN and email != "":
        with sql.connect("UserDatabase.db") as con:
            cur = con.cursor()
            sql_query = """DELETE FROM Users WHERE email=?"""
            data = [email]
            cur.execute(sql_query, data)
            con.commit()
            msg = "User successfully deleted"
    else:
        msg = "User not deleted"
    return render_template("new_result.html", msg=msg)

@app.route('/clearuserlogin')
def clearUserLogin():
    #global LOGIN, user_role, login_email
    LOGIN = user.GetLogin()
    if LOGIN:
        login_email = ""
        user.SetEmail(login_email)
        LOGIN = False
        user.SetLogin(LOGIN)
        user_role = "Customer"
        user.SetRole(user_role)
        msg = "Log Out Successful"
        # return render_template("SuccessfulLogout.html")
    else:
        msg = "You're not logged in, please log in first."
        # return render_template("UnSuccessfulLogout.html")
    return render_template("new_result.html", msg=msg)


@app.route('/searchproducts')
def search_product():
    IsLoggedIn = user.GetLogin()
    usersRole = user.GetRole()
    
    if IsLoggedIn:
        if usersRole == 'Warehouse' or usersRole == 'Authenticator':
            return render_template("searchproducts.html")
        
        elif usersRole == 'Customer':

            msg = "You do not have permissions to access this page."
        
        else:
            msg = "This message should not be displayed. Something went wrong somewhere. This message is printed from WebAppForUsers.py in the function new_product()"
        
    else:

        msg = "You're not logged in, please log in first."
        
    return render_template("new_result.html", msg=msg)
        

@app.route('/usersearch', methods=['POST', 'GET'])
def user_search():
    prod_name = request.form['prod_name']

    # search_prod.SetName(prod_name)

    # with sql.connect("InventoryDatabase.db") as con:
    #     cur = con.cursor()
    #     sql_query = """select prod_id from Inventory where prod_name=?"""
    #     data = [prod_name]
    #     cur.execute(sql_query, data)
    #     prod_id = cur.fetchall();
    #     prod_id = prod_id[0][0]
    
    # search_prod.SetID(prod_id)

    # with sql.connect("InventoryDatabase.db") as con:
    #     con.row_factory = sql.Row
    #     cur = con.cursor()
    #     sql_query = """select * from Inventory where prod_name=?"""
    #     data = [prod_name]
    #     cur.execute(sql_query, data)
    #     user_search = cur.fetchall();
    #     msg = "Product successfully found"
    #     print(user_search)
    #     if len(user_search) != 0:
    #         print(user_search)
    #         return render_template('dispsearchprod.html', user_search=user_search)
    #     else:
    #         msg = "No products found"
    #         return render_template("new_result.html", msg=msg)

    inventoryTable = dynamoDB.inventory_returnAllRecordData()
    print(prod_name)
    result = dynamoDB.singleQuery_returnAllDataForASingleQuery(keyID='prod_ID', queryParam='Space', whichTable="Inventory")
    # print(result)

    return render_template('dispsearchprod.html', user_search=result)

@app.route('/editprod')
def dispProdInfo():
    authenticated = ['Yes', 'No']
    return render_template('EditProductPage.html', authenticated=authenticated)

@app.route('/editprodinfo', methods=['POST', 'GET'])
def edit_product():
    # Fetches information from html form

    prod_name = search_prod.GetName()
    print(prod_name)
    price = request.form['price']
    desc = request.form['desc']
    quantity = request.form['quantity']
    auth = request.form['auth']

    with sql.connect("InventoryDatabase.db") as con:
        cur = con.cursor()
        sql_query = """Update Inventory set price=?,desc=?,quantity=?,auth=? where prod_name=?"""
        data = (price,desc,quantity,auth,prod_name)
        cur.execute(sql_query, data)
        con.commit()
        msg = "Record successfully edited"
    return render_template("new_result.html", msg=msg)

@app.route('/deleteprod')
def delete_product():
    prod_name = search_prod.GetName()
    prod_id = search_prod.GetID()
    with sql.connect("InventoryDatabase.db") as con:
        cur = con.cursor()
        sql_query = """DELETE FROM Inventory WHERE prod_name=?"""
        data = [prod_name]
        cur.execute(sql_query, data)
        con.commit()
        msg = "Product successfully deleted"

        s3 = boto3.resource('s3')

        bucket = bucket_names_object.bucket_names_object()

        temp_url = s3_bucket_operations.getUrlForOneProd(prod_id)
        new_file = temp_url.split('/')

        length = len(new_file) - 1
        print(new_file[length])
        refac_file = new_file[length]

        temp_ext = refac_file.split('.')
        length = len(temp_ext) - 1
        ext = temp_ext[length]

        source_file = prod_id + "." + ext

        s3.Object(bucket.getSourceBucketName, source_file).delete()
        s3.Object(bucket.getRefactoredBucketName, refac_file).delete()


    return render_template("new_result.html", msg=msg)










if __name__ == '__main__':
    # global LOGIN
    #global LOGIN, user_role, login_email

    LOGIN = False
    user_role = "Customer"
    login_email = ""

    user = user_login_obj(LOGIN, login_email, user_role)

    prod_id = ""
    prod_name = ""

    search_prod = product_info_obj(prod_id, prod_name)

    #dynamoDB.testForUsersDynamoDB()

    app.run(debug=True)  # Starts the app in debug mode


