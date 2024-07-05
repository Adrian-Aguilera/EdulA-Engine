from openai import OpenAI
import ollama
from dotenv import load_dotenv
import os

class LModel():
    def __init__(self, api_key, model_point):
        self.client = OpenAI(base_url=model_point, api_key=api_key)
        self.modelo= os.environ.get('MODELLM')
    
    async def _callGenerate(self, system_content,message_user, data=None, ):
        output = []
        responseCall = await ollama.generate(
            model=self.modelo,
            prompt=f"{system_content}{data}. Responde a este mensaje: {message_user}",
            stream=True,
        )
        for fragmento in responseCall:
            output.append(fragmento["response"], end='', flush=True)
        
        return output
    async def av_chat(self, mode, system_content, message_user):
        return message_user
    
    async def response_general(self, mode, system_content, message_user):
        
        return message_user