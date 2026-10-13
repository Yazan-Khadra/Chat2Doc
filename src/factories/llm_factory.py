from abc import ABC , abstractmethod

class LLMInterface(ABC):

    @abstractmethod
    def set_generation_model(self , model_id: str):

        raise NotImplementedError

    @abstractmethod
    def generate(self , prompt: str , max_output_tokens : str, chat_history: list = [],
    temperature: float = 0.2):

        raise NotImplementedError

    @abstractmethod
    def construct_prompt(self , prompt: str , role: str):

        raise NotImplementedError

    @abstractmethod
    def set_embedding_model(self , model_id: str):
        raise NotImplementedError

    @abstractmethod
    def embed_text(self , text: str , document_type: str):

        raise NotImplementedError

        
    