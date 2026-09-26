from enum import Enum

class ResponseSignal(Enum):

    FILE_UPLOADED_SUCCESS = 'File Uploaded Succesfully'
    FILE_TYPE_VALIDATED_FAILED = "File Type not Valid"
    FILE_SIZE_VALIDATED_FAILED =  "File Size not Valid"
