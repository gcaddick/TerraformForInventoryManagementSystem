import boto3



def queryADynamoDBTable():
    return None

def inventory_returnAllRecordData():

    dynamodbUSERS = boto3.resource('dynamodb')
    table = dynamodbUSERS.Table('Inventory')
    allDataFromDynamoDBtable = table.scan(Select='ALL_ATTRIBUTES')
    recordsWithinAllDataFromDynamoDBtable = allDataFromDynamoDBtable['Items']

    return recordsWithinAllDataFromDynamoDBtable

def users_returnAllRecordData():

    dynamodbUSERS = boto3.resource('dynamodb')
    table = dynamodbUSERS.Table('Users')
    allDataFromDynamoDBtable = table.scan(Select='ALL_ATTRIBUTES')
    recordsWithinAllDataFromDynamoDBtable = allDataFromDynamoDBtable['Items']

    return recordsWithinAllDataFromDynamoDBtable

def testForUsersDynamoDB():
    dynamodbUSERS = boto3.resource('dynamodb')#, endpoint_url="https://dynamodb.eu-west-2.amazonaws.com")

    table = dynamodbUSERS.Table('Users')

    allDataFromDynamoDBtable = table.scan(Select='ALL_ATTRIBUTES')

    recordsWithinAllDataFromDynamoDBtable = allDataFromDynamoDBtable['Items']
    # Above output (data replaced with hashes): [{'city': '#', 'user_id': '#', 'last_name': '#', 'role': '#', 'first_name': '#', 'date_joined': '#', 'address': '#', 'email': '#', 'pword': '#'}, {'city': '#', 'user_id': '#', 'last_name': '#', 'role': '#', 'first_name': '#', 'date_joined': '#', 'address': '#', 'email': '#', 'pword': '#'}]

    # print(recordsWithinAllDataFromDynamoDBtable)

    # for record in recordsWithinAllDataFromDynamoDBtable:
    #     print(record['city'])

def InsertNewProducts(prod_id, prod_name, price, desc, quantity, auth, temp_url):
    dynamodbUSERS = boto3.resource('dynamodb', 'eu-west-2')
    table = dynamodbUSERS.Table('Inventory')
    response = table.put_item(
       Item={
           'prod_ID' : prod_id,
           'prod_name' : prod_name,
           'price' : price,
           'desc' : desc,
           'quantity' : quantity ,
           'auth' : auth,
           'prod_url' : temp_url
       })
    return response

def InsertNewUsers(user_id, email, fn, ln, pword, date_joined, addr, city, role):

    dynamodbUSERS = boto3.resource('dynamodb', 'eu-west-2')
    table = dynamodbUSERS.Table('Users')
    response = table.put_item(
       Item={
           'user_id' : user_id,
           'email' : email,
           'first_name' : fn,
           'last_name' : ln,
           'pword' : pword ,
           'date_joined' : date_joined,
           'address' : addr,
           'city' : city,
           'role' : role
       })
    return response

