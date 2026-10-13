from ..llm_factory import LLMInterface
from openai import OpenAI
import logging
from typing import Optional


class OpenAIProvider(LLMInterface):

    def __init__(self , api_key: str , api_url: None,
                 deafult_input_max_characters: int=1000,
                 deafult_generation_max_output_tokens: int=1000,
                 temperature: float=0.2):
        self.api_key = api_key
        self.api_url = self.api_url
        self.deafult_input_max_characters = deafult_input_max_characters
        self.deafult_generation_max_output_tokens = deafult_generation_max_output_tokens
        self.deafult_temperature = temperature
        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_model_dims = None

        self.client = OpenAI(
            api_key = self.api_key,
            base_url= self.api_url
        )
        self.logger = logging.getLogger(__name__)


    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str , dims: int):
        self.embedding_model_id = model_id
        self.embedding_model_dims = dims

        

    def embed_text(self, text: str, document_type: str):
        if not self.client:

            self.logger.error("OpenAI client was not set")
            return None
        if not self.embedding_model_id:
            self.logger.error("Embedding model for OpenAI Was Not Set")
            return None

        response = self.client.embeddings.create(
            model= self.embedding_model_id,
            input=text
        )
        if not response or not response.data or len(response.data) ==0 or not response.data[0].embedding:
            self.logger.error("Error while embedding text with OpenAI")

            return None
        return response.data[0].embedding


    def generate(self, prompt: str, max_output_tokens: Optional[int] = None , chat_history:list=[], temperature: float = 0.2):

        if not self.client:
            self.logger.error("OpenAI client was not set")
            return None
        if not self.generation_model_id:
            self.logger.error("Generation model was not set")
            return None

        max_output_tokens = max_output_tokens if max_output_tokens else self.deafult_generation_max_output_tokens
        temperature = temperature if temperature else self.deafult_temperature


    def construct_prompt(self, prompt: str, role: str):
        return {
            "role":role,
            "content":prompt
        }







    



