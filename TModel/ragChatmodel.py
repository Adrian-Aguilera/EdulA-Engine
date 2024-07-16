import ollama
import chromadb
from chromadb.config import Settings

conversation_history = []

def callModelcustom(user_message):
    global conversation_history
    
    # Añadimos el mensaje del usuario a la lista de historial de conversación
    conversation_history.append({'role': 'user', 'content': user_message})

    # Primero intentamos obtener una respuesta relevante de la base de datos RAG
    rag_response = query_rag(user_message)
    
    if rag_response:
        conversation_history.append({'role': 'assistant', 'content': rag_response})

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

def query_rag(prompt):
    configuracion = Settings(is_persistent=True, persist_directory="./DB/Chroma_storageDB")
    client = chromadb.Client(settings=configuracion)
    collectionInter = client.get_or_create_collection(name="Tcollection")

    responseInput = ollama.embeddings(
        prompt=prompt,
        model="mxbai-embed-large"
    )
    results = collectionInter.query(
        query_embeddings=[responseInput["embedding"]],
        n_results=1
    )

    if results['documents']:
        data = results['documents'][0][0]
        print(f'Resultados de la DB: {data}')
        return data
    else:
        return None

def initialize_rag_db():
    partes_exposicion_fisica = [
        "Adrián: Investigar los conceptos del tema, estudiarlos para explicarlos y agregarlos a la presentación: -Que es un vector? -cuales son las componentes de un vector? -que representa un vector en el plano (x,y) -que es la cinemática? -Como se aplica la cinemática en los vectores -que es el en movimiento en dos dimensiones? -que es el movimiento en tres dimensiones? -qué es el movimiento en tres dimensiones? -cómo se aplican los vectores en dos dimensiones y que representan? -cómo se aplican los vectores en tres dimensiones y que representan?",
        "Oscar: investigar y desarrollar un ejercicio de vectores en dos dimensiones, hacer el ejercicio con procesos y luego agregarlo detalladamente a la presentación para explicarlo en la presentación",
        "Andrew: investigar y desarrollar ejercicio de vectores en dos y tres dimensiones y agregarlo a la presentación para explicarlo en la presentación -Desarrollar simulador para vectores para presentarlo en la presentación",
        "Didier: investigar ejercicio de vectores en tres dimensiones y agregarlo a la presentación de la exposición"
    ]

    configuracion = Settings(is_persistent=True, persist_directory="./DB/Chroma_storageDB")
    client = chromadb.Client(settings=configuracion)
    collectionInter = client.get_or_create_collection(name="Tcollection")

    for i, d in enumerate(partes_exposicion_fisica):
        response = ollama.embeddings(model="mxbai-embed-large", prompt=d)
        embedding = response["embedding"]
        collectionInter.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[d]
        )

if __name__ == "__main__":
    initialize_rag_db()  # Inicializa la base de datos RAG

    while True:
        mensaje = input('Ingresa una duda: ')
        callModelcustom(user_message=mensaje)
