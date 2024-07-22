import ollama
from openai import OpenAI
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
import os
load_dotenv()


def enbedings():
    embedings = ollama.embeddings(
        model='mxbai-embed-large',
        prompt='Hola mucho como estas?',
    )
    print(embedings)

def clientChromaIntern(path):
    pass
def rag_option():
    texto_exposicion_fisica = """
    Adrián: Investigar los conceptos del tema, estudiarlos para explicarlos y agregarlos a la presentación:
    - Que es un vector?
    - Cuales son las componentes de un vector?
    - Que representa un vector en el plano (x,y)
    - Que es la cinemática?
    - Como se aplica la cinemática en los vectores
    - Que es el en movimiento en dos dimensiones?
    - Que es el movimiento en tres dimensiones?
    - Qué es el movimiento en tres dimensiones?
    - Cómo se aplican los vectores en dos dimensiones y que representan?
    - Cómo se aplican los vectores en tres dimensiones y que representan?

    Oscar: investigar y desarrollar un ejercicio de vectores en dos dimensiones, hacer el ejercicio con procesos y luego agregarlo detalladamente a la presentación para explicarlo en la presentación

    Andrew: investigar y desarrollar ejercicio de vectores en dos y tres dimensiones y agregarlo a la presentación para explicarlo en la presentación
    - Desarrollar simulador para vectores para presentarlo en la presentación

    Didier: investigar ejercicio de vectores en tres dimensiones y agregarlo a la presentación de la exposición
    """

    # Divide el texto en partes usando un delimitador, en este caso, una línea en blanco
    partes_exposicion_fisica = texto_exposicion_fisica.strip().split('\n\n')

    configuracion = Settings(is_persistent=True, persist_directory="./DB/Chroma_storageDB")
    # Configurar Chroma para usar almacenamiento persistente
    client = chromadb.Client(settings=configuracion)
    #collection = client.create_collection(name="db_embeding")
    collectionInter = client.get_or_create_collection(name="Tcollection")

    # store each document in a vector embedding database
    for i, d in enumerate(partes_exposicion_fisica):
        response = ollama.embeddings(model="mxbai-embed-large", prompt=d.strip())
        embedding = response["embedding"]
        collectionInter.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[d.strip()]
        )
    prompt = "Que hace Didier? y que es lo que tiene que investigar"

    # generate an embedding for the prompt and retrieve the most relevant doc
    responseInput = ollama.embeddings(
        prompt=prompt,
        model="mxbai-embed-large:latest"
    )
    results = collectionInter.query(
        query_embeddings=[responseInput["embedding"]],
        n_results=1
    )
    data = results['documents'][0][0]
    print(f'resultados de la db: {data}')
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    output = ollama.generate(
        model="llama2:7b",
        prompt=f"Usa esta informacion: {data}. Responde a este mensaje: {prompt}",
        stream=True,
    )

    for pieza in output:
        print(pieza["response"], end='', flush=True)

if __name__=="__main__":
    rag_option()
    '''
    is_persistent = os.environ.get("ISPERSISTENT", "false").lower() in ("true", '1', 't')
    if is_persistent:
        print('true')
    else:
        print('false')'''