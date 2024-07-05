from Modules.LModel import *
from dotenv import load_dotenv
import os

#cargando variables de entorno
load_dotenv()
class ControllerEduIA:
    
    def __init__(self, EngineAV=None, EngineChat=None):
        self.EngineAV =EngineAV
        self.EngineChat = EngineChat
        self.key = os.environ.get('API_KEY')
        self.model_url = os.environ.get('MODEL_URL')
        self.Model = os.environ.get('MODEL')
        self.sys_content = os.environ.get('SYS_CONTENT')
    
    
    async def Edula_AV(self, message):
        edula_av = 'modulo para asistente virtual'
        return edula_av
    
    async def Edula_General(self, message):
        # Cargar clase con parámetros necesarios
        Lmodel = LModel(api_key=self.key, model_point=self.model_url)
        
        fun_model = await Lmodel.response_chat(model=self.Model, sys_content=self.sys_content, message_user=message)
        message_user = fun_model
        
        return  message_user

    async def main_engine(self, message):
        if self.EngineAV:
            return await self.Edula_AV(message)
        elif self.EngineChat:
            return await self.Edula_General(message)
        else:
            return "Motor no encontrado"