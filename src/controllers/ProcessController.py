from .BaseController import BaseController

from .ProjectController import ProjectController

from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader


from models import ProcessingEnum , ResponseSignal

import logging
logger = logging.getLogger(__name__)

class ProcessController(BaseController):

    def __init__(self , project_id: str):

        super().__init__()

        self.project_id = project_id

        self.project_path = ProjectController().get_project_path(project_id)

    def get_file_extension(self , file_id : str):

        file_path = Path(file_id)

        file_extension = file_path.suffix

        return file_extension

    def get_file_loader(self , file_id: str):

        file_path = self.project_path / file_id
        file_extension = self.get_file_extension(file_id)
        

        if file_extension == ProcessingEnum.TXT_EXTENSION.value:

            return TextLoader(file_path , encoding = "utf-8")

        elif file_extension == ProcessingEnum.PDF_EXTENSION.value:

            return PyMuPDFLoader(file_path)

        else:
            return None

    def get_file_content(self , file_id: str):

        file_loader = self.get_file_loader(file_id = file_id)

        if file_loader is None:

            logger.warning("unsupported File Type .Project ID: %s , File ID %s",self.project_id , file_id)

            return []

        try:
            return file_loader.load() 

        except FileNotFoundError:
            logger.warning(
                "File exists in database but is missing from disk. "
                "Project ID: %s, File ID: %s, Expected path: %s",
                self.project_id,
                file_id,
                self.project_path / file_id,
            )
            return []
        except Exception:
            logger.exception(
                "Failed to load file. Project ID: %s, File ID: %s",
                 self.project_id,
                 file_id,
            )







