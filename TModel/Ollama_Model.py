import ollama
from openai import OpenAI
import chromadb
from chromadb.config import Settings


def enbedings():
    embedings = ollama.embeddings(
        model='mxbai-embed-large',
        prompt='Hola mucho como estas?',
    )
    print(embedings)
    
def rag_option():
    partes_exposicion_fisica = [
        "Adrián: Investigar los conceptos del tema, estudiarlos para explicarlos y agregarlos a la presentación: -Que es un vector? -cuales son las componentes de un vector? -que representa un vector en el plano (x,y) -que es la cinemática? -Como se aplica la cinemática en los vectores -que es el en movimiento en dos dimensiones? -que es el movimiento en tres dimensiones? -qué es el movimiento en tres dimensiones? -cómo se aplican los vectores en dos dimensiones y que representan? -cómo se aplican los vectores en tres dimensiones y que representan?",
        "Oscar: investigar y desarrollar un ejercicio de vectores en dos dimensiones, hacer el ejercicio con procesos y luego agregarlo detalladamente a la presentación para explicarlo en la presentación",
        "Andrew: investigar y desarrollar ejercicio de vectores en dos y tres dimensiones y agregarlo a la presentación para explicarlo en la presentación -Desarrollar simulador para vectores para presentarlo en la presentación",
        "Didier: investigar ejercicio de vectores en tres dimensiones y agregarlo a la presentación de la exposición"
    ]

    # Configurar Chroma para usar almacenamiento persistente
    settings = Settings(persist_directory="./DB/Chroma_storageDB")
    client = chromadb.Client(settings=settings)
    collection = client.create_collection(name="db_embeding")

    # store each document in a vector embedding database
    for i, d in enumerate(partes_exposicion_fisica):
        response = ollama.embeddings(model="mxbai-embed-large", prompt=d)
        embedding = response["embedding"]
        collection.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[d]
        )
    prompt = "Que hace Didier? y que es lo que tiene que investigar"

    # generate an embedding for the prompt and retrieve the most relevant doc
    response = ollama.embeddings(
        prompt=prompt,
        model="mxbai-embed-large"
    )
    results = collection.query(
        query_embeddings=[response["embedding"]],
        n_results=1
    )
    data = results['documents'][0][0]
    output = ollama.generate(
        model="llama2:7b",
        prompt=f"Usa esta informacion: {data}. Responde a este mensaje: {prompt}",
        stream=True,
    )

    for pieza in output:
        print(pieza["response"], end='', flush=True)

if __name__=="__main__":
    rag_option() 