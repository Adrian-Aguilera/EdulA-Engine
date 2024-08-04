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
from .models import DataChromaGeneral, configChromaGeneral
import logging

logger = logging.getLogger('EduApp')
load_dotenv(override=True)

class ControllerInter():
    # Hacer que main_engine sea síncrono, llamando async_to_sync dentro de él
    def main_engine(type_engine, message):
        if not type_engine:
            return "Faltan parámetros para inicializar el motor"

        engine_av = type_engine.get("EngineAV", None)
        engine_general = type_engine.get("EngineGeneral", None)

        if engine_av is not None:
            engine = ControllerEduIA(EngineAV=engine_av)
            mensaje = async_to_sync(engine.main_engine)(message)
            logger.error(f"Error in get_general_chat: {mensaje}")
            return mensaje

        elif engine_general is not None:
            engine = ControllerEduIA(EngineChat=engine_general)
            mensaje = async_to_sync(engine.main_engine)(message)
            logger.error(f"Error in get_general_chat: {mensaje}")
            return mensaje
        else:
            return "Tipo de motor no definido correctamente"

class GeneralEdula(APIView):
    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'type_engine': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'EngineAV': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'EngineGeneral': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    },
                    required=['EngineAV', 'EngineGeneral']
                ),
                'mesage': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['type_engine', 'mesage']
        )
    )
    @api_view(["POST"])
    @permission_classes([IsAuthenticated])
    def get_general_chat(request):
        if request.method == "POST":
            try:
                data_requests = request.data
                type_engine_data = data_requests.get('type_engine')
                message = data_requests.get('mesage')
                if type_engine_data:
                    engine = ControllerInter.main_engine(type_engine_data, message)
                    return JsonResponse({"data": engine})
                else:
                    return Response({"error": "Error engine activate"})

            except Exception as e:
                return Response({"error": f"{str(e)}"})
        else:
            return Response({"error": "metodo no disponible"})


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
                #print(f'data: {getDataContent}')
                response = dbController.createDatabase(nameCollection=getNameCollection, dataContent=getDataContent)
                return JsonResponse(response)
            except Exception as e:
                return Response({"Error": f"{str(e)}"})
        else:
            return Response({"error": "metodo no disponible"})