from openai import OpenAI
import ollama
from dotenv import load_dotenv
import os

load_dotenv()
class LModel:
    def __init__(self, api_key, model_point):
        self.client = OpenAI(base_url=model_point, api_key=api_key)
        self.modelo = os.environ.get("MODELLM")
        self.modelEmbedding= os.environ.get("MODELEMBEDDING")

    async def _callGenerate(self, system_content, message_user, embeddings=None):
        output = []
        responseCall = await ollama.generate(
            model=self.modelo,
            prompt=f"{system_content}{embeddings}. Responde a este mensaje: {message_user}",
            stream=True,
        )
        for fragmento in responseCall:
            output.append(fragmento["response"], end="", flush=True)

        return output

    async def av_chat(self, mode, system_content, message_user):
        return message_user

    async def response_general(self, mode, system_content, message_user):
        try:
            embeddings = "embeddings"
            response = self._callGenerate(system_content=system_content, message_user=message_user, )
            if response:
                return {"message": response}
        except Exception as e:
            return {"error": "Error al conectar la motor"}
        return message_user

    async def _callEmbeding(self,promt):
        try:
            reponseEmbeddings = ollama.embeddings(
                prompt=promt,
                model=self.modelEmbedding
            )
            return reponseEmbeddings
        except Exception as e:
            return str(e)
