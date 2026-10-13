from .ProcessController import ProcessController 
from langchain_text_splitters import RecursiveCharacterTextSplitter

from models import ProcessingEnum , ResponseSignal
import logging
logger = logging.getLogger(__name__)

class RecursiveChunkController(ProcessController):

    def __init__(self , project_id):
        super().__init__(project_id)

    
    def process_file_content_by_recursive_text_splitter(self, file_id : str
     , chunk_size : int = 100 , overlap_size : int = 20):

        file_content = self.get_file_content(file_id)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size= chunk_size,
            chunk_overlap= overlap_size,
            length_function=len,

        )

        if not file_content:
            logger.warning(
                "Skipping chunking because file content is empty. "
                "Project ID: %s, File ID: %s",
                self.project_id,
                file_id,
            )

            return (
                False,
                ResponseSignal.FILE_PROCESSING_FAILED.value,
                [],
                [],
            )

        # extract the text form the file_content
        file_content_texts = [record.page_content for record in file_content]

        # get the metadaa from the file_content
        file_content_metadata = self.process_file_metadata(file_content)

        # generate chunks
        chunks = self.generate_chunks(text_splitter , file_content_texts , file_content_metadata)

        # check if process success
        is_success , message = self.test_chunking_success(chunks)

        chunks_response = [
        {
        "page_content": chunk.page_content,
        "metadata": chunk.metadata
        }
    for chunk in chunks
]
    
        return is_success , message , chunks_response , chunks



    def process_file_metadata(self , file_content : list):

        file_content_metadata = [record.metadata for record in file_content]

        return file_content_metadata


    def generate_chunks(self , text_splitter:RecursiveCharacterTextSplitter , file_content_texts:list , file_content_metadata:list):

        chunks = text_splitter.create_documents(
            file_content_texts,
            metadatas=file_content_metadata
        )

        return chunks

    def test_chunking_success(self , chunks):

        if chunks is None or len(chunks) == 0:

            return False , ResponseSignal.FILE_PROCESSING_FAILED.value

        return True , ResponseSignal.FILE_PROCESSING_SUCCESS.value


