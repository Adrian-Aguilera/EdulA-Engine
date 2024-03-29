import requests
import json
from dotenv import load_dotenv
import os
load_dotenv()
"""prueba usando la api de gemini atraves de API_rest"""
api_key = os.environ.get('API_KEY')
proyecto_id = os.environ.get('proyecto_id')

def enviar_solicitud(json_data):
    headers = {
        'Content-Type': 'application/json',
    }

    params = {
        'key': f'{api_key}',
    }

    response = requests.post(
        'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent',
        params=params,
        headers=headers,
        json=json_data,
    )

    # Extrae el texto generado de la respuesta
    texto_generado = json.loads(response.content)

    return texto_generado

def iniciar_conversacion():
    texto = "Hola! Soy un chatbot creado con la API de Gemini."
    print(texto)

    while True:
        mensaje_usuario = input("Tú: ")

        json_data = {
            'contents': [
                {
                    'parts': [
                        {
                            'text': f'{mensaje_usuario}',
                        },
                    ],
                },
            ],
        }
        # Envía el mensaje del usuario a la API de Gemini
        respuesta_gemini = enviar_solicitud(json_data)
        
        print("Gemini:", respuesta_gemini)

iniciar_conversacion()
