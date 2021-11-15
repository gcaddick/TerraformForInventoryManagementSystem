import boto3
import bucket_names_object
import time


def getFileNamesOfObjectsWithinAnS3Bucket(nameOfS3BucketToBeCalled):
    # Grabs list of all objects (names) [images in our case] from either our source or refactored S3 bucket
    # Returns a list of the names of all objects within an S3 bucket
    # "getFromSourceBucket" -> If true, get the items from the stock bucket, if not we would only want to get it from the refactored bucket

    nameOfBucketToBeUsedToPullDataFrom = determineTheBucketAndReturnTheBucketName(nameOfS3BucketToBeCalled)

    objectRepresentingAnS3Bucket = boto3.resource('s3')
    my_bucket = objectRepresentingAnS3Bucket.Bucket(nameOfBucketToBeUsedToPullDataFrom)
    allObjectsFromRefactoredBucket = my_bucket.objects.all()

    listOfObjectsAttainedFromGivenS3Bucket = []
    for objects in allObjectsFromRefactoredBucket:

        # # DEBUG - Following prints format of 'allObjectsFromRefactoredBucket'
        # print("Object: {}".format(allObjectsFromRefactoredBucket))

        listOfObjectsAttainedFromGivenS3Bucket.append(objects.key)
        # objects.key is the name of the file in the s3 bucket within current iteration

    # print(listOfObjectsAttainedFromGivenS3Bucket)

    return listOfObjectsAttainedFromGivenS3Bucket

def getURLOfONEObjectWithinAnS3Bucket(nameOfS3BucketToBeCalled, nameOfObjectFile):
    # This function will return a single URL of the object [file] from a public S3 bucket
    # This is achieved using concatenation of a URL that is used to access S3 items, but with the irrelevant information removed and the relevant included.

    defaultUrl = "https://<BUCKET-NAME>.s3.<REGION-NAME>.amazonaws.com/<NAME-OF-FILE>"
    theRegionOfOurBuckets = "eu-west-2"

    objectURL = defaultUrl.replace("<BUCKET-NAME>", nameOfS3BucketToBeCalled)
    objectURL = objectURL.replace("<REGION-NAME>", theRegionOfOurBuckets)
    objectURL = objectURL.replace("<NAME-OF-FILE>", nameOfObjectFile)

    # Debug - final URL for an object
    # print("Debug final URL for an object: " + objectURL)

    return objectURL

def getAllObjectsURLsFromS3AsList(nameOfS3BucketToBeCalled):
    # Will return all objects [images] from an S3 bucket [source/refactored] as a list

    nameOfS3BucketToBeCalled = determineTheBucketAndReturnTheBucketName(nameOfS3BucketToBeCalled)

    listOfAllTheNamesOfObjectsWithinAnS3Bucket = getFileNamesOfObjectsWithinAnS3Bucket(nameOfS3BucketToBeCalled)

    listOfAllTheURLsOfObjectsWithinAnS3Bucket = []

    for objectName in listOfAllTheNamesOfObjectsWithinAnS3Bucket:

        getTheUrlOfObjectInCurrentIteration = getURLOfONEObjectWithinAnS3Bucket(nameOfS3BucketToBeCalled, objectName)

        listOfAllTheURLsOfObjectsWithinAnS3Bucket.append(getTheUrlOfObjectInCurrentIteration)

    return listOfAllTheURLsOfObjectsWithinAnS3Bucket


def determineTheBucketAndReturnTheBucketName(nameOfS3BucketToBeCalled):
    # Will return the correct bucket name, and if it does not match, then raise an exception

    sourceBucket = "source-image-bucket-5623"
    refactoredBucket = "refactored-image-bucket-5623"

    if nameOfS3BucketToBeCalled == sourceBucket:
        return sourceBucket
    elif nameOfS3BucketToBeCalled == refactoredBucket:
        return refactoredBucket
    else:
        raise ValueError("Inputted S3 bucket name does not match any within the function: 'determineTheBucketAndReturnTheBucketName' in s3_bucket_operations.py")


def getUrlForOneProd(prod_id):
    time.sleep(5)
    """Get a list of keys in an S3 bucket and return URL for specific product item."""
    s3 = boto3.client('s3')
    keys = []
    new_object = bucket_names_object.bucket_names_object()
    refactored_bucket = new_object.getRefactoredBucketName
    s3_resource = boto3.resource('s3')
    s3_bucket = s3_resource.Bucket(refactored_bucket)

    fileNameSplit = prod_id.split(".") # Splits the filename to get the extension
    filename = fileNameSplit[0]
    filename = filename + "_"

    resp = s3.list_objects_v2(Bucket=refactored_bucket)
    for obj in resp['Contents']:
        keys.append(obj['Key'])

    for key in keys:
        if filename in key:
            path_name = getURLOfONEObjectWithinAnS3Bucket(refactored_bucket, key)
    return path_name