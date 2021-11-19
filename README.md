# TerraformForInventoryManagementSystem

Project:

To make an inventory management system using AWS services

This application allows you to:

Add new products
-Search Products
-User Info
-Edit Account
-Register
-Login
-Logout

Registering a user as a “Warehouse” account will allow you to have administrative privileges when using the application. You have an option to select the type of account, via a drop down menu, when on the account registration page. Alternatively, you can select the option to register as a “Customer”, which will then limit your privileges. 

This project has two branches in this GitHub repository: 

main - This is the version of the application which runs a local SQlite (whether deployed locally or on an EC2 instance).

EC2DevBranch - This is the version of the application which runs on AWS using an EC2 instance, a NAT gateway, VPCs, an elastic IP, and DynamoDB. Unfortunately this branch was not completed as we had run out of time to iron out all of the issues we were experiencing. A lot of the infrastructure and code is already working and tested, but not all.

- DynamoDB is completely integrated
- VPCs, NAT gateway, VPCs, Elastic IP are working together as intended

There are two databases that are being utilised in this project: “Users” and “Inventory”.

The User database contains the following data: 
- User ID (user_id)
- Address (address)
- City (city)
- Date Joined (date_joined)
- Email (email)
- First Name (first_name)
- Last Name (last_name)
- Password (pword)
- Role (role)

The Inventory database contains the following data:
- Product ID (prod_id)
- Authenticated (auth)
- Description (desc)
- Price (price)
- Product Authentication 


Initialisation:

There are two ways to run the program, first using an EC2 instance and the user-data to launch the website. The second, is running the python file manually using the command: python3 WebAppForUsers.py

For the first option, Terraform needs to be installed. The user-data file downloads the required python files and html templates from an S3 bucket and launches the website on start-up, therefore only needing to connect to the website via the EC2 instance public IPv4.

To launch the website the second way, the required packages need to be installed first, this is done via the command: pip install -r requirements.txt. Then run the website by using the command: python3 WebAppForUsers.py
 
