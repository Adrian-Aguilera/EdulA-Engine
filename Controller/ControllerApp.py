from Modules.IAModel import *
from dotenv import load_dotenv
import os
#cargando variables de entorno
load_dotenv()
class ControllerEduIA:
    
    def __init__(self, EngineAV=None, EngineChat=None):
        self.EngineAV =EngineAV
        self.EngineChat = EngineChat
    async def edulaAV(self, message):
        edula_av = 'modulo para asistente virtual'
        return edula_av

    async def edulaGeneral(self, message):
        # Cargar clase con parámetros necesarios
        Lmodel = LModel()
        fun_model = await Lmodel.responseGeneral(message_user=message)
        message_user = fun_model
        return  message_user

    async def main_engine(self, message):
        if self.EngineAV:
            return await self.edulaAV(message)
        elif self.EngineChat:
            return await self.edulaGeneral(message)
        else:
            return "Motor no encontrado"