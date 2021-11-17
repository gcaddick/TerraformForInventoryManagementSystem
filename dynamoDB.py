import boto3
from boto3.dynamodb.conditions import Key


def singleQuery_returnAllDataForASingleQuery(queryParam, whichTable):
    table = returnCorrectTable(whichTable=whichTable)

    response = table.query(
        KeyConditionExpression=Key('prod_name'),
        FilterExpression= 'Space'
    )

    # response = table.query(KeyConditionExpression= boto3.dynamodb.conditions.Key(queryParam))
    return response

def returnCorrectTable(whichTable):
    if whichTable == 'Inventory':
        dynamodbUSERS = boto3.resource('dynamodb')
        table = dynamodbUSERS.Table('Inventory')
        return table
    elif whichTable == 'Users':
        dynamodbUSERS = boto3.resource('dynamodb')
        table = dynamodbUSERS.Table('Users')
        return table
    else:
        return "This should not execute"


def inventory_returnAllRecordData():

    dynamodbInventory = boto3.resource('dynamodb')
    table = dynamodbInventory.Table('Inventory')
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

