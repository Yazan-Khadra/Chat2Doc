from fastapi import UploadFile

from models import ResponseSignal

from .BaseController import BaseController

from .ProjectController import ProjectController

from pathlib import Path

import aiofiles

import re

import os

class DataController(BaseController):
    def __init__(self):
        super().__init__()

    def validate_file_type(self, uploaded_file: UploadFile) -> bool:

        # check if the file type is valid

        return uploaded_file.content_type in self.app_settings.ALLOWED_FILE_TYPES

    def validate_file_size(self, uploaded_file: UploadFile) -> bool:

        return uploaded_file.size <= self.app_settings.ALLOWED_FILE_SIZE * 1024 * 1024
        

    def validate_input(self, uploaded_file: UploadFile):

        type_is_valid = self.validate_file_type(uploaded_file=uploaded_file)

        if type_is_valid == False:
            return False, ResponseSignal.FILE_TYPE_VALIDATED_FAILED

        size_is_valid = self.validate_file_size

        if size_is_valid == False:
            return False, ResponseSignal.FILE_SIZE_VALIDATED_FAILED

        return True, ResponseSignal.FILE_UPLOADED_SUCCESS

    # save the file on the path given
    async def save_file(self , project_path : Path , file : UploadFile):
        # define the unique file name
        file_name = self.generate_unique_file_name(original_file_name = file.filename)
        # defined the file path
        file_path = project_path / file_name
        # save the file chunk by chunk
        async with aiofiles.open(file_path , "wb") as f:
            while chunk := await file.read(self.app_settings.CHUNK_SIZE):
                await f.write(chunk) 
        return file_name

    def generate_unique_file_name(self , original_file_name: str):
        # generate unique file name 
        random_file_name = self.generate_random_string()
        # get the new file name
        new_file_name = self.get_cleaned_filename(original_file_name)

        # get the last file name result
        new_file_name = random_file_name + "_" + new_file_name

        return new_file_name



    def get_cleaned_filename(self , original_file_name:str):
        # remove the special characters
        cleaned_file_name = re.sub(r'[^\w.]' , '',original_file_name.strip())

        # replace spaces with underscore
        cleaned_file_name = cleaned_file_name.replace(" " , "_")

        return cleaned_file_name








