from Modules.LModel import *
from dotenv import load_dotenv
import os

#cargando variables de entorno
load_dotenv()
class ControllerEduIA:
    def __init__(self, EngineAV=None, EngineChat=None):
        self.EngineAV =EngineAV
        self.EngineChat = EngineChat
    
    def credenciales(self):
        key = os.environ.get('API_KEY')
        model_url = os.environ.get('MODEL_URL')
        Model = os.environ.get('MODEL')
        sys_content = os.environ.get('SYS_CONTENT')
        return key, model_url, Model, sys_content
    
    def Edula_AV(self, message):
        edula_av = 'modulo para asistente virtual'
        return edula_av+message
    
    def Edula_Chat(self, message):
        #modelo_url = "http://localhost:1234/v1"
        # Importando credenciales
        key, model_url, Model, sys_content = self.credenciales() 
        # Cargar clase con parámetros necesarios
        Lmodel = LModel(api_key=key, model_point=model_url)
        
        fun_model = Lmodel.response_chat(model=Model, sys_content=sys_content, message_user=message)
        message_user = fun_model
        
        return  message_user
    
    def main_engine(self, message):
        if self.EngineAV:
            return self.Edula_AV(message)
        elif self.EngineChat:
            return self.Edula_Chat(message)
        else:
            return "Motor no encontrado"