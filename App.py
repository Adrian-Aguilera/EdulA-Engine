from Modules.ControllerApp import *
import os

if __name__ == "__main__":
    #inicializando controlador
    Engine = ControllerEduIA(EngineAV=True, EngineChat=False)
    print(Engine.main_engine()) #llamamos clase principal