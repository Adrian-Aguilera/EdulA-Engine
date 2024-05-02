# Create your views here.
from django.shortcuts import render
from Modules.LModel import *
from Controller.ControllerApp import *
from django.http import HttpResponse
from dotenv import load_dotenv
import os

#importacion de django-rest.
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

#cargando variables de entorno
load_dotenv()

def main_engine(type_engine, message):
    engine = ControllerEduIA(EngineAV=type_engine.get('EngineAV', False), EngineChat=type_engine.get('EngineChat', False))
    model_main = engine.main_engine(message)
    return model_main


@api_view(["POST"])
@permission_classes([IsAuthenticated])  
def get_response(request):
    if request.method == "POST":
        try:
            data_requests = request.data
            type_engine_data = data_requests.get('type_engine')
            message = data_requests.get('mesage', '')
            engine = main_engine(type_engine_data, message)
            return Response({"data": engine})
        except Exception as e:
            return Response({"error": f"{str(e)}"})
    else:
        return Response({"error": "metodo utilizado es distinto a POST"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def test(request):
    if request.method == "POST":
        return Response({'respuesta': True})
    else:
        return Response({'fail': False})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_option(request):
    if request.method == "GET":
        return Response({"respuesta": "GET"})
    else:
        return Response({"Error": "Metodo no disponible"})
