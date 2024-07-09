from ollama import Client
import subprocess

ollama = Client(host='127.0.0.1:11434')

def modelCUSTOM():
    modelfile = '''
    FROM llama2:7b
    PARAMETER temperature 0.5
    SYSTEM Eres un asistente virtual creado por ITCA FEPADE en El Salvador y solo hablas en español. Tu función es proporcionar asistencia estrictamente en temas educativos. Debes mantener un enfoque educativo en todas tus respuestas y evitar la alucinación o respuestas fuera de tema.
    '''

    test = ollama.create(model='generalITCA2', modelfile=modelfile)
    print(test) 
 

# Inicializamos una lista para almacenar los mensajes de la conversación
conversation_history = []

def callModelcustom(user_message):
    global conversation_history
    
    # Añadimos el mensaje del usuario a la lista de historial de conversación
    conversation_history.append({'role': 'user', 'content': user_message})
    
    # Llamamos al modelo con el historial de conversación completo
    stream = ollama.chat(
        model='generalITCA2',
        messages=conversation_history,
        stream=True,
        options={'num_ctx': 150}
    )

    # Procesamos y mostramos la respuesta del modelo
    response_content = ""
    for chunk in stream:
        response_content += chunk['message']['content']
        print(chunk['message']['content'], end='', flush=True)
    print('\n')
    
    # Añadimos la respuesta del modelo al historial de conversación
    conversation_history.append({'role': 'assistant', 'content': response_content})

if __name__ == "__main__":
    #print(ollama.show('GeneralItca'))
    #modelCUSTOM()
    while True:
        mensaje = input('Ingresa una duda: ')   
        callModelcustom(user_message=mensaje)
        
 
        
    
    