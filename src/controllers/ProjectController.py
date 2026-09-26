

from .BaseController import BaseController

from pathlib import Path

class ProjectController(BaseController):

    def __init__(self):

        super().__init__()

    def get_project_path(self , project_id : str):

        project_path = self.file_path / project_id

        project_path.mkdir(parents=True, exist_ok=True)

        return project_path


        

        