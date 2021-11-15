import s3_bucket_operations

class contains_all_urls_for_s3_buckets:
    #

    def __init__(self, hasAllBucketNamesObject):
        self._listOfAllObjectURLsFromSourceBucket = None
        self._listOfAllObjectURLsFromRefactoredBucket = None
        self._hasAllBucketNamesObject = hasAllBucketNamesObject  # This is fixed once object is initialised

        # On initialisation get all object URLs for each Bucket

        self._listOfAllObjectURLsFromSourceBucket = s3_bucket_operations.\
            getAllObjectsURLsFromS3AsList(hasAllBucketNamesObject.getSourceBucketName)

        self._listOfAllObjectURLsFromRefactoredBucket = s3_bucket_operations.\
            getAllObjectsURLsFromS3AsList(hasAllBucketNamesObject.getRefactoredBucketName)

    @property
    def getListOfAllObjectURLsFromSourceBucket(self):
        return self._listOfAllObjectURLsFromSourceBucket

    @property
    def getListOfAllObjectURLsFromRefactoredBucket(self):
        return self._listOfAllObjectURLsFromRefactoredBucket

    # Purpose of functions below is to be called when new items have been uploaded to S3, they need to be called
    # with a !DELAY! [to give time after upload has occured]
    def triggerSourceBucketUpdate(self):
        self._listOfAllObjectURLsFromSourceBucket = s3_bucket_operations. \
            getAllObjectsURLsFromS3AsList(self._hasAllBucketNamesObject.getSourceBucketName)

    def triggerRefactoredBucketUpdate(self):
        self._listOfAllObjectURLsFromRefactoredBucket = s3_bucket_operations.\
            getAllObjectsURLsFromS3AsList(self._hasAllBucketNamesObject.getRefactoredBucketName)