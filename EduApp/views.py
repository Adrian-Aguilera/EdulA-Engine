from django.shortcuts import render
from Modules.IAModel import *
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
import logging

logger = logging.getLogger('EduApp')
load_dotenv(override=True)

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

class MainOption(APIView):
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
                message = data_requests.get('mesage', '')
                if type_engine_data:
                    engine = main_engine(type_engine_data, message)
                    return JsonResponse({"data": engine})
                else:
                    return Response({"error": "Error engine activate"})

            except Exception as e:
                return Response({"error": f"{str(e)}"})
        else:
            return Response({"error": "metodo no disponible"})


    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id_users': openapi.Schema(type=openapi.TYPE_STRING),
                'type_engine': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'EngineAV': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    },
                    required=['EngineAV']
                ),
                'id_message': openapi.Schema(type=openapi.TYPE_STRING),
                'user_message': openapi.Schema(type=openapi.TYPE_STRING),
                'history_chat': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'system_response': openapi.Schema(type=openapi.TYPE_STRING),
                        'user_response': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                ),
            },
            required=['id_users', 'type_engine', 'id_message', 'user_message']
        )
    )
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def get_response_AV(request):
        if request.method == "POST":
            try:
                data_response = unpack_json(data_input=request)
                if not data_response:
                    return Response({"Fail": "Json invalido"})
                else:
                    id_users, type_engine, id_message, user_message = data_response

                    engine = main_engine(type_engine, user_message)
                    return Response({"data": f"{engine}"})
            except Exception as e:
                return Response({"Error": "Fail get data"})
        else:
            return Response({"error": "metodo no disponible"})

def unpack_json(data_input):
    try:
        data_requests = data_input.data
        id_users = data_requests.get("id_users")
        type_engine = data_requests.get("type_engine")
        id_message = data_requests.get("id_message")
        user_message = data_requests.get("user_message")
        return id_users, type_engine, id_message, user_message
    except TypeError:
        return None
