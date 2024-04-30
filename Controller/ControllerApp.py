from Modules.LModel import *
from dotenv import load_dotenv
import os

#cargando variables de entorno
load_dotenv()
class ControllerEduIA:
    def __init__(self, EngineAV=None, EngineChat=None):
        self.EngineAV =EngineAV
        self.EngineChat = EngineChat
    def Edula_AV(self):
        edula_av = 'modulo para asistente virtual'
        return edula_av
    
    def Edula_Chat(self):
        key = os.environ.get('API_KEY')
        model_point = os.environ.get('MODEL_POINT')
        Model = os.environ.get('MODEL')
        sys_content = os.environ.get('SYS_CONTENT')
        Lmodel = LModel(api_key=key, model_point=model_point)
        
    
    def main_engine(self):
        if self.EngineAV:
            return self.Edula_AV()
        elif self.EngineChat:
            return self.Edula_Chat()
        else:
            return "Motor no encontrado"