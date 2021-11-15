class bucket_names_object:

    def __init__(self):
        # Purpose of this class is to have one location for the bucket names, so that if there is a change
        # in bucket names, only the following variables need to be adjusted [SINGLETON].
        self._sourceBucket = "source-image-bucket-5623"
        self._refactoredBucket = "refactored-image-bucket-5623"


    @property
    def getSourceBucketName(self):
        return self._sourceBucket

    @property
    def getRefactoredBucketName(self):
        return self._refactoredBucket