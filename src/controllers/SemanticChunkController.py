from .ProcessController import ProcessController

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_experimental.text_splitter import SemanticChunker

from models import ProcessingEnum, ResponseSignal


class SemanticChunkController(ProcessController):

    _embedding_model = None

    def __init__(self, project_id):
        super().__init__(project_id)

    def process_file_content_by_semantic_text_splitter(
        self,
        file_id: str,

    ):
        
        # Get embedding model
        embeddings = self.get_embedding_model()

        # Get file content
        file_content = self.get_file_content(file_id)

        # Extract text
        file_content_texts = self.process_file_content(
            file_content
        )

        # Extract metadata
        file_metadata = self.process_file_metadata(
            file_content
        )

        # Initialize semantic text splitter
        text_splitter = SemanticChunker(
            embeddings=embeddings,
            breakpoint_threshold_type="percentile",
            breakpoint_threshold_amount=66,
            buffer_size=1,
            min_chunk_size=300,
            sentence_split_regex=r"(?<!\bDr\.)(?<!\bMr\.)(?<!\bMrs\.)(?<!\bProf\.)(?<=[.?!])\s+",
            add_start_index=True,
        )

        # Generate chunks
        chunks = self.generate_chunks(
            text_splitter,
            file_content_texts,
            file_metadata
        )
       

        # Check process success
        is_success, message = self.test_chunking_success(
            chunks
        )

        chunks_response = [
                        {
                        "page_content": chunk.page_content,
                        "metadata": chunk.metadata
                        }
                    for chunk in chunks
                ]

        return is_success, message, chunks_response

    def get_embedding_model(self):

        if self._embedding_model is None:

            self._embedding_model = HuggingFaceEmbeddings(
                model_name="BAAI/bge-base-en-v1.5",
                model_kwargs={
                    "device": "cpu"
                },
                encode_kwargs={
                    "normalize_embeddings": True
                }
            )

        return self._embedding_model

    def process_file_metadata(
        self,
        file_content: list
    ):

        return [
            record.metadata
            for record in file_content
        ]

    def process_file_content(
        self,
        file_content: list
    ):

        return [
            record.page_content
            for record in file_content
        ]

    def test_chunking_success(
        self,
        chunks
    ):

        if chunks is None or len(chunks) == 0:
            return (
                False,
                ResponseSignal.FILE_PROCESSING_FAILED.value
            )

        return (
            True,
            ResponseSignal.FILE_PROCESSING_SUCCESS.value
        )

    def generate_chunks(
        self,
        text_splitter: SemanticChunker,
        file_content_texts: list,
        file_content_metadata: list
    ):

        chunks = text_splitter.create_documents(
            file_content_texts,
            metadatas=file_content_metadata
        )

        return chunks