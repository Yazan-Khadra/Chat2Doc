from fastapi import FastAPI , APIRouter , Depends , UploadFile , status
from fastapi.responses import JSONResponse
from helpers.config import get_settings , Settings
from controllers import DataController , ProjectController

data_router = APIRouter(
    prefix= '/api/v1/data',
    tags= ['api_v1' , 'data']
)

@data_router.post('/upload/{project_id}')
async def upload_file(project_id: str , uploaded_file : UploadFile , app_settings : Settings=Depends(get_settings)):

    

    # validate the user input
    
    data_controller_object = DataController()

    is_type_valid , message = data_controller_object.validate_input(uploaded_file)

    if is_type_valid == False:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {
                "message" : message.value
            }
        )

    # validate the project path
    
     # define object from ProjectController
    project_controller = ProjectController()
     # get the project path
    project_path = project_controller.get_project_path(project_id)
    # save the uploaded file into the project path
    file_name = await data_controller_object.save_file(project_path , uploaded_file)

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {
            "message" : message.value,
            'file_name': file_name
            
        }
    )

