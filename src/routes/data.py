
from fastapi import APIRouter, Depends, Request, UploadFile, status
from fastapi.responses import JSONResponse
import os
import logging
from helpers.config import get_settings, Settings

from controllers import (
    DataController,
    ProjectController,
    RecursiveChunkController,
    SemanticChunkController,
)

from .schemes.data import ProcessRequest, SemanticChunkProcessRequest

from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.AssetModel import AssetModel
from models.db_schemes.asset import Asset
from models import AssetTypeEnum
from models.db_schemes.data_chunk import DataChunk
from models import ResponseSignal

logger = logging.getLogger('uvicorn.error')
data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"],
)


@data_router.post("/upload/{project_id}")
async def upload_file(
    request: Request,
    project_id: str,
    uploaded_file: UploadFile,
    app_settings: Settings = Depends(get_settings),
):
    # Create project model object
    project_model = await ProjectModel.create_instance(
        request.app.state.mongo_db
    )

    # Create or get project
    project = await project_model.get_or_create(project_id=project_id)

    # Validate user input
    data_controller_object = DataController()

    is_type_valid, message = data_controller_object.validate_input(
        uploaded_file
    )

    if not is_type_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": message.value,
            },
        )

    # Create ProjectController object
    project_controller = ProjectController()

    # Get project path
    project_path = project_controller.get_project_path(project_id)

    # Save uploaded file
    file_name, file_path = await data_controller_object.save_file(
        project_path,
        uploaded_file,
    )

    # Store asset in the database
    asset_model = await AssetModel.create_instance(
        db_client=request.app.state.mongo_db
    )

    asset_resources = Asset(
        asset_project_id=project.id, # type: ignore
        asset_type=AssetTypeEnum.FILE.value,
        asset_name=file_name,
        asset_size=os.path.getsize(file_path),
    )

    asset_record = await asset_model.create_asset(
        asset=asset_resources
    )

    print(file_name)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": message.value,
            "file_id": file_name,
        },
    )


@data_router.post("/process/{project_id}/recursive-chunk")
async def recursive_chunk_process(
    request: Request,
    project_id: str,
    process_request: ProcessRequest,
):
    # Extract data from process request
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset

    # Get project model
    project_model = await ProjectModel.create_instance(
        request.app.state.mongo_db
    )

    # Get or create project
    project = await project_model.get_or_create(
        project_id=project_id
    )
    asset_model = await AssetModel.create_instance(
        db_client=request.app.state.mongo_db
    )

    if file_id:


        asset_record = await asset_model.get_asset_record(
            asset_project_id=project.id, # type: ignore
            asset_name = file_id
        )
        if asset_record is None:
            return JSONResponse(
                status_code = status.HTTP_400_BAD_REQUEST,
                content ={
                    "message" : ResponseSignal.FILE_ID_ERROR.value
                }
            )
        project_files_ids = {
            asset_record.id : asset_record.asset_name
        }

    else:
        

        project_files = await asset_model.get_all_project_assets(
            asset_project_id=project.id,  # type: ignore
            asset_type=AssetTypeEnum.FILE.value,
        )

        project_files_ids = {
            record.id : record.asset_name
            for record in project_files
        }

        if len(project_files_ids) == 0:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.NO_FILES_ERROR.value,
                },
            )

    num_records = 0
    num_files = 0
    message = None
    chunks = []
    all_files_chunks = []

    for _id,file_id in project_files_ids.items(): # type: ignore
        # Start processing
        (
            is_success,
            message,
            chunks,
            file_chunks,
        ) = RecursiveChunkController(
            project_id
        ).process_file_content_by_recursive_text_splitter(
            file_id=file_id,
            chunk_size=chunk_size,
            overlap_size=overlap_size,
        )

        if file_chunks is None:
            logger.error(f"Error while Processing file: {file_id}")
            continue

        if not is_success:
            logger.warning(
                "Skipping file. Project ID: %s, File ID: %s, Reason: %s",
                project_id,
                file_id,
                message,
            )
            continue

        else:
            project_object_id = project.id

            if project_object_id is None:
                raise ValueError(
                    "Project has no MongoDB ObjectId"
                )

            file_chunks_records = [
                DataChunk(
                    chunk_text=chunk.page_content,
                    chunk_metadata=chunk.metadata,
                    chunk_order=i + 1,
                    chunk_project_id=project_object_id,
                    chunk_asset_id=_id # type: ignore
                )
                for i, chunk in enumerate(file_chunks)
            ]

            all_files_chunks.append(chunks)

            chunk_model = await ChunkModel.create_instance(
                db_client=request.app.state.mongo_db
            )

            num_records += await chunk_model.insert_many_chunks(
                chunks=file_chunks_records
            )

            num_files += 1

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": message,
            "number_of_records": num_records,
            "number_of_files": num_files,
            "chunks": all_files_chunks,
        },
    )


@data_router.post("/process/{project_id}/semantic-chunk")
async def semantic_chunk_process(
    project_id: str,
    process_request: SemanticChunkProcessRequest,
):
    # Extract file ID from request
    file_id = process_request.file_id

    # Start processing
    is_success, message, chunks = (
        SemanticChunkController(
            project_id
        ).process_file_content_by_semantic_text_splitter(
            file_id=file_id
        )
    )

    if not is_success:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": message,
            },
        )

    else:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": message,
                "chunks": chunks,
            },
        )