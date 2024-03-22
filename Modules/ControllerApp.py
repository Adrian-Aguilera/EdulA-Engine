from Modules.DotEnv import *
#variable = DotEnv().dotenv("model")
class ControllerEduIA:
    def __init__(self, EngineAV=None, EngineChat=None):
        self.EngineAV =EngineAV
        self.EngineChat = EngineChat
    def Edula_AV(self):
        edulaAV = "Modulo para Asistente virtual"
        return edulaAV
    def Edula_Chat(self):
        edulachat="Modulo para Conversacion inteligente"
        return edulachat
    def main_engine(self):
        if self.EngineAV:
            return self.Edula_AV()
        elif self.EngineChat:
            return self.Edula_Chat()
        else:
            return "Motor no encontrado"