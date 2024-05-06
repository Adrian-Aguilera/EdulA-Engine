# Create your views here.
from django.shortcuts import render
from Modules.LModel import *
from Controller.ControllerApp import *
from dotenv import load_dotenv
from asgiref.sync import async_to_sync

#importacion de django-rest.
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

#cargando variables de entorno
load_dotenv()

def main_engine(type_engine, message):
    if not type_engine:
        return "Faltan parámetros para inicializar el motor"

    engine_av = type_engine.get("EngineAV", None)
    engine_chat = type_engine.get("EngineChat", None)

    if engine_av is not None:
        engine = ControllerEduIA(EngineAV=engine_av)
        return async_to_sync(engine.main_engine)(message)

    elif engine_chat is not None:
        engine = ControllerEduIA(EngineChat=engine_chat)
        return async_to_sync(engine.main_engine)(message)
    else:
        return "Tipo de motor no definido correctamente"

#parametros para el swagger
@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'type_engine': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'EngineAV': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'EngineChat': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                },
                required=['EngineAV', 'EngineChat']
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
            engine = main_engine(type_engine_data, message)
            return Response({"data": engine})
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
def get_response_AV(requests):
    if requests.method == "POST":
        try:
            data_response = unpack_json(data_input=requests)
            if not data_response:
                return Response({"Fail": "Json invalido"})
            else:
                id_users, type_engine, id_message, user_message = data_response
                
                #la informacion de estas variables viene de la db  y se retorna al front
                """
                    history_system,
                    history_user
                """
                #llamada a las funciones
                engine = main_engine(type_engine, user_message)
                return Response({"data": f"{engine}"})
        except Exception as e:
            return Response({"Error": "Fail get data"})
    else:
        return Response({"error": "metodo no disponible"})


#desenpaquetar json
def unpack_json(data_input):
    try:
        data_requests = data_input.data
        id_users= data_requests.get("id_users")
        type_engine = data_requests.get("type_engine")
        id_message = data_requests.get("id_message")
        user_message = data_requests.get("user_message")
        """
        history_system = data_requests.get("history_chat").get("system_response")
        history_user = data_requests.get("history_chat").get("user_response")
        """ 
        return id_users, type_engine, id_message, user_message
    except TypeError:
        return None