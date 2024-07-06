# Create your views here.
from django.shortcuts import render
from Modules.IAModel import *
from Controller.ControllerApp import *
from dotenv import load_dotenv
from asgiref.sync import async_to_sync

#importacion de django-rest.
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView

class CustomModel(APIView):
    #enp para crear un modelCustom
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def createModelCustom(requests):
        return Response({'response': 'modelo creado exitosamente'})