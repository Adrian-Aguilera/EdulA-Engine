import ollama
from openai import OpenAI
import chromadb

def  message():
    while True:
        messages = []
        user_input = input("mensaje: ")
        messages.append({"role": "system", "content": "eres un tutor digital diseñado por la institucion ITCA fepade de el salvador, ayudas a los estudiantes en cualquier duda, y solo hablas español!"})

        messages.append({"role": "user", "content": user_input})
        
        response = ollama.chat(model='llama2:chat', messages=messages, stream=True)
        
        for chunk in response:
            chat_response = chunk['message']['content']
            print(chunk['message']['content'], end='', flush=True)
        messages.append({"role": "assistant", "content": chat_response})
        
        print("\n")
        if user_input == "salir":
            break


def enbedings():
    embedings = ollama.embeddings(
        model='mxbai-embed-large',
        prompt='Hola mucho como estas?',
    )
    print(embedings)
    
def rag_option():
    documents_linkedin = [
        "Componentes de la base de datos no relacional que usa Linkedin (mongoDB): Esquema de datos: El esquema de datos que utiliza LinkedIn es el siguiente: LinkedIn es una red social profesional que almacena una gran cantidad de datos de usuarios, incluidos perfiles, conexiones, mensajes, publicaciones, interacciones y más.",
        "Si LinkedIn optara por utilizar MongoDB como su base de datos, podría organizar los datos de la siguiente manera: Colecciones principales: Usuarios: Cada usuario tendría un documento en esta colección que contendría información básica del perfil, como nombre, foto, experiencia laboral, educación, habilidades, etc.",
        "Conexiones: Esta colección podría contener documentos que mapean las relaciones de conexión entre los usuarios. Cada documento podría tener campos como ID del usuario, ID de conexión y posiblemente algún tipo de información adicional sobre la relación.",
        "Colecciones auxiliares: Mensajes: LinkedIn permite a los usuarios enviar mensajes entre ellos, podría haber una colección para almacenar estos mensajes. Cada documento podría contener información sobre el remitente, el destinatario, el contenido del mensaje, la marca de tiempo, etc.",
        "Publicaciones: los usuarios pueden realizar publicaciones en LinkedIn, podría haber una colección para almacenar estas publicaciones. Cada documento podría contener información sobre el autor, el contenido de la publicación, los comentarios, las reacciones, etc.",
        "Índices: Se crearían índices para mejorar el rendimiento de las consultas comunes, como buscar usuarios por nombre, buscar conexiones de un usuario dado, encontrar mensajes entre dos usuarios, etc.",
        "Escalabilidad Horizontal con MongoDB Atlas: MongoDB Atlas es una solución de base de datos en la nube que permite escalar sus bases de datos en cualquier dirección.",
        "Replicación: MongoDB ofrece capacidades de replicación que permiten crear copias idénticas de los datos en múltiples nodos. Esto mejora la disponibilidad, la redundancia y distribuye la carga de lectura entre los nodos replicados.",
        "Sharding: MongoDB distribuye la carga de trabajo entre fragmentos de un clúster fragmentado. Cada fragmento procesa un subconjunto de operaciones del clúster.",
        "Sharding permite escalar horizontalmente tanto la carga de lectura como la de escritura, agregando más fragmentos según sea necesario.",
        "Aplicar sharding para distribuir eficientemente la carga de datos de usuarios y actividades.",
        "Escalabilidad Horizontal: MongoDB puede crear nuevos nodos fácilmente, como si fueran replicaciones del propio MongoDB. Esto permite distribuir la carga de trabajo entre varios nodos o clústeres.",
        "LinkedIn podría aprovechar esta escalabilidad horizontal para manejar el crecimiento constante de usuarios y datos",
        "Seguridad y privacidad: Seguridad: Autenticación y autorización: Implementar mecanismos de autenticación y autorización para proteger los datos de los usuarios",
        "Encriptación: Encriptar los datos sensibles para protegerlos de accesos no autorizados.",
        "Auditoría: Implementar auditoría para rastrear las actividades en la plataforma.",
        "Privacidad: Control de acceso: Permitir a los usuarios controlar la privacidad de sus datos.",
        "Consentimiento: Obtener el consentimiento de los usuarios antes de recopilar y usar sus datos.",
        "Eliminación de datos: Permitir a los usuarios eliminar sus datos de la plataforma."
    ]


    client = chromadb.Client()
    collection = client.create_collection(name="docs")

    # store each document in a vector embedding database
    for i, d in enumerate(documents_linkedin):
        response = ollama.embeddings(model="mxbai-embed-large", prompt=d)
        embedding = response["embedding"]
        collection.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[d]
        )
        
    # an example prompt
    prompt = "que pasaria si linkedin usara mongoDB"

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
    
    # generate a response combining the prompt and data we retrieved in step 2
    output = ollama.generate(
        model="llama2:chat",
        prompt=f"Using this data: {data}. Respond to this prompt: {prompt}",
        stream=True,
    )

    for pieza in output:
        print(pieza['message']['content'], end='', flush=True)

if __name__=="__main__":
    rag_option() 