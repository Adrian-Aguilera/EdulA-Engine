import google.generativeai as genai
from dotenv import load_dotenv
import os

"""prueba usando la api de gemini atraves de la libreria de google"""
def configure_api():
    load_dotenv()
    api_key = os.environ.get('API_KEY')
    genai.configure(api_key=api_key)

def iniciar_chat():
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])
    return chat

def enviar_mensaje(chat, mensaje):
    response = chat.send_message(f"{mensaje}", stream=True)
    for chunk in response:
        print(chunk.text)
        print("_"*120)

def main():
    configure_api()
    chat = iniciar_chat()
    
    while True:
        mensaje = input("tu: ")
        if mensaje.lower() == "salir":
            print("Chat finalizado.")
            break
        enviar_mensaje(chat, mensaje)

if __name__ == "__main__":
    main()
