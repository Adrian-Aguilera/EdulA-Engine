from Modules.IAModel import GeneralModel
from dotenv import load_dotenv
import os

# Cargando variables de entorno
load_dotenv(override=True)

class ControllerEduIA:
    def __init__(self, EngineAV=None, EngineChat=None):
        self.EngineAV = EngineAV
        self.EngineChat = EngineChat

    async def edulaAV(self, message):
        edula_av = 'modulo para asistente virtual'
        return edula_av

    async def edulaGeneral(self, message):
        # Cargar clase con parámetros necesarios
        modelGeneral = GeneralModel()
        fun_model = await modelGeneral.responseGeneral(message_user=message)
        return fun_model

    async def main_engine(self, message):
        if self.EngineAV:
            return await self.edulaAV(message)
        elif self.EngineChat:
            return await self.edulaGeneral(message)
        else:
            return "Motor no encontrado"
