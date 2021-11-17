import boto3
from boto3.dynamodb.conditions import Key, Attr


def singleQuery_returnAllDataForASingleQuery(keyID, whichTable, queryParam=None):
    table = returnCorrectTable(whichTable)
    
    if queryParam == None: # return all data in column
        response = table.scan(AttributesToGet=[keyID])
        response = response['Items']
    
    else:
        response = table.scan(FilterExpression=Attr('prod_name').contains(queryParam))
        response = response['Items']

    return response


def returnCorrectTable(whichTable):
    if whichTable == 'Inventory':
        dynamodbUSERS = boto3.resource('dynamodb', 'eu-west-2')
        table = dynamodbUSERS.Table('Inventory')
        return table
    elif whichTable == 'Users':
        dynamodbUSERS = boto3.resource('dynamodb', 'eu-west-2')
        table = dynamodbUSERS.Table('Users')
        return table
    else:
        return "This should not execute"


def inventory_returnAllRecordData():

    dynamodbInventory = boto3.resource('dynamodb', 'eu-west-2')
    table = dynamodbInventory.Table('Inventory')
    allDataFromDynamoDBtable = table.scan(Select='ALL_ATTRIBUTES')
    recordsWithinAllDataFromDynamoDBtable = allDataFromDynamoDBtable['Items']

    return recordsWithinAllDataFromDynamoDBtable

def users_returnAllRecordData():

    dynamodbUSERS = boto3.resource('dynamodb', 'eu-west-2')
    table = dynamodbUSERS.Table('Users')
    allDataFromDynamoDBtable = table.scan(Select='ALL_ATTRIBUTES')
    recordsWithinAllDataFromDynamoDBtable = allDataFromDynamoDBtable['Items']

    return recordsWithinAllDataFromDynamoDBtable

def testForUsersDynamoDB():
    dynamodbUSERS = boto3.resource('dynamodb', 'eu-west-2')#, endpoint_url="https://dynamodb.eu-west-2.amazonaws.com")

    table = dynamodbUSERS.Table('Users')

    allDataFromDynamoDBtable = table.scan(Select='ALL_ATTRIBUTES')

    recordsWithinAllDataFromDynamoDBtable = allDataFromDynamoDBtable['Items']
    # Above output (data replaced with hashes): [{'city': '#', 'user_id': '#', 'last_name': '#', 'role': '#', 'first_name': '#', 'date_joined': '#', 'address': '#', 'email': '#', 'pword': '#'}, {'city': '#', 'user_id': '#', 'last_name': '#', 'role': '#', 'first_name': '#', 'date_joined': '#', 'address': '#', 'email': '#', 'pword': '#'}]

    # print(recordsWithinAllDataFromDynamoDBtable)

    # for record in recordsWithinAllDataFromDynamoDBtable:
    #     print(record['city'])

def InsertNewProducts(prod_id, prod_name, price, prod_desc, quantity, prod_auth, temp_url):
    dynamodbUSERS = boto3.resource('dynamodb', 'eu-west-2')
    table = dynamodbUSERS.Table('Inventory')
    response = table.put_item(
       Item={
           'prod_ID' : prod_id,
           'prod_name' : prod_name,
           'price' : price,
           'prod_desc' : prod_desc,
           'quantity' : quantity ,
           'prod_auth' : prod_auth,
           'prod_url' : temp_url
       })
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        msg = "Product Successfully Added"
    else:
        msg = "Error Adding Product"
    return msg

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
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        msg = "User Successfully Added"
    else:
        msg = "Error Adding User"
    return msg


def delete_products_db(whichTable, prod_id):
    table = returnCorrectTable(whichTable)
    response = table.delete_item(
        Key={
            'prod_ID' : prod_id
        }
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        msg = "Product Successfully Deleted"
    else:
        msg = "Error Deleting Product"
    return msg

def updating_products_db(whichTable, prod_id, prod_name, price, prod_desc, quantity, prod_auth):
    dynamodbUSERS = boto3.resource('dynamodb', 'eu-west-2')
    table = dynamodbUSERS.Table('Inventory')
    response = table.update_item(
        Key={
            'prod_ID': prod_id
        },
        UpdateExpression="set price=:p, prod_desc=:d, quantity=:q, prod_auth=:a",
        ExpressionAttributeValues={
            ':p': price,
            ':d': prod_desc,
            ':q': quantity,
            ':a': prod_auth
        },
        ReturnValues="UPDATED_NEW"
        )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        msg = "Product Successfully Updated"
    else:
        msg = "Error Updating Product"
    return msg


def delete_user_db(email, whichTable):
    table = returnCorrectTable(whichTable)
    response = table.scan(filterExpression=Attr('email').contains(email)
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        msg = "Product Successfully Deleted"
    else:
        msg = "Error Deleting Product"
    return msg