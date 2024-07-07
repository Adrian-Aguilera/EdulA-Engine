# Create your views here.
from django.shortcuts import render
from Modules.IAModel import *
from Controller.ControllerApp import *
from dotenv import load_dotenv
from asgiref.sync import async_to_sync
import subprocess
#importacion de django-rest.
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView

#ollama module
from ollama import Client

ollamaClient = Client(host='127.0.0.1:11434')
class CustomModel(APIView):
    #enp para crear un modelCustom
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def createModelCustom(request):
        if request.method == "POST":
            try:
                dataRequests = request.data['modelfile']
                modelfile = f'''
                    FROM {dataRequests['modelo']}
                    PARAMETER temperature {float(dataRequests['temperatura'])}
                    SYSTEM {dataRequests['systemContent']}
                '''
                modelName = dataRequests['nombre']
                ollamaResponse = callCreateModel(modelName=modelName, modelfile=modelfile)
                return Response(ollamaResponse)
            except Exception as e:
                return Response({'Error': f'{str(e)}'})
        else:
            return Response({'ErrorMethod': 'Metodo no permitido'})
    
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def showAllModel(request):
        if request.method == 'GET':
            try:
                modelAvailable = ollamaClient.list()  #subprocess.run("ollama list", shell=True)
                return Response({"Models": modelAvailable})
            except Exception as e:
                return Response({"Error": "Error al motrar modelos"})
        else:
            return Response({"Method": "Metodo no disponible    "})
                
        
        
def callCreateModel(modelName,modelfile):
    try:
        ollmaResponse = ollamaClient.create(model=modelName, modelfile=modelfile)
        if ollmaResponse['status'] == "success":
            return {"response": "modelo creado correctamente"}
        else:
            return {"error": "error al crear modelo"}
    except Exception as e:
        return {"FatalError": f"Error al conectar ollma {str(e)}"}
            