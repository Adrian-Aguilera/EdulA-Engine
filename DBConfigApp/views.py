from django.shortcuts import render
from Modules.GeneralModel import *
from Controller.ControllerApp import *
from dotenv import load_dotenv
from asgiref.sync import sync_to_async
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from .models import DataChromaGeneral
from EduGeneralApp.models import configChromaGeneral

#clase que se encargara de gestionar la parte de la informacion de los modelos
class DataToChromaDB(APIView):
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def activateGeneralMode(request):
        if request.method == "GET":
            try:
                dbController = ControllerDataBase()
                configInstance = configChromaGeneral.objects.all()
                getNameCollection = configInstance[0].nameCollection
                getDataContent = DataChromaGeneral.objects.all()[0].dataContent
                print(f'data: {getNameCollection}')
                response = dbController.createDatabase(nameCollection=getNameCollection, dataContent=getDataContent)
                return JsonResponse(response)
            except Exception as e:
                return Response({"Error": f"{str(e)}"})
        else:
            return Response({"error": "metodo no disponible"})