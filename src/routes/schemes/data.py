from pydantic import BaseModel

from fastapi import UploadFile

from typing import Optional

class ProcessRequest(BaseModel):

    file_id : Optional[str] = None
    chunk_size : int = 100
    overlap_size : int = 20
    do_reset : Optional[int] = 0

class SemanticChunkProcessRequest(BaseModel):

    file_id: str
    

