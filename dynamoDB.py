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

