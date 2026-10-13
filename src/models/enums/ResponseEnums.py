from enum import Enum

class ResponseSignal(Enum):

    FILE_UPLOADED_SUCCESS = 'File Uploaded Succesfully'
    FILE_TYPE_VALIDATED_FAILED = "File Type not Valid"
    FILE_SIZE_VALIDATED_FAILED =  "File Size not Valid"
    FILE_PROCESSING_FAILED = "File Processing Failed"
    FILE_PROCESSING_SUCCESS = "File PRocessing Success"
    NO_FILES_ERROR = "not found any files"
    FILE_ID_ERROR = "no file with this id"
