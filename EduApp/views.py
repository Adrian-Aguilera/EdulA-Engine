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

def main_engine(request):
    Engine = ControllerEduIA(EngineAV=False, EngineChat=True)
    return Engine

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def test(request):
    if request.method == "POST":
        return Response({'respuesta': True})
    else:
        return Response({'fail': False})
