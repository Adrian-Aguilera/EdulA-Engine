from langchain_core.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
from llama_index.service_context import ServiceContext
from llama_index import VectorStoreIndex
from langchain_community.chat_models import ChatAnyscale
from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
import chromadb
from embedings import Embeding


# Carga documentos desde un directorio
path = r'C:\Users\cruz7\Downloads\data'
loader = DirectoryLoader(path, glob="**/*.txt", loader_cls=TextLoader)
print("Instanciando cargador")
documentos = loader.load()
print(documentos)

text="""
PARTES PARA EXPOSICION DE FISICA
Adrián: Investigar los conceptos del tema, estudiarlos para explicarlos y agregarlos
a la presentación:
-Que es un vector?
-cuales son las componentes de un vector?
-que representa un vector en el plano (x,y)
-que es la cinemática?
-Como se aplica la cinemática en los vectores
-que es el en movimiento en dos dimensiones?
-que es el movimiento en tres dimensiones?
-que es el movimiento en tres dimensiones?
-cómo se aplican los vectores en dos dimensiones y que representan?
-cómo se aplican los vectores en tres dimensiones y que representan?

Oscar: investigar y desarrollar un ejercicio de vectores en dos dimensiones, hacer el
ejercicio con procesos y luego agregarlo detalladamente a la presentación para
explicarlo en la presentación

Andrew: investigar y desarrollar ejercicio de vectores en dos y tres dimensiones y
agregarlo a la presentación para explicarlo en la presentación
-Desarrollar simulador para vectores para presentarlo en la presentación

Didier: investigar ejercicio de vectores en tres dimensiones y agregarlo a la
presentación de la exposición
"""

# Divide los documentos en fragmentos más pequeños
text_splitter = RecursiveCharacterTextSplitter(chunk_size=30, chunk_overlap=10)
# print(text_splitter)
fragmentos = text_splitter.split_documents(documentos)

""""
# Obtén los embeddings para los fragmentos
embeddings = OpenAIEmbeddings(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
    model="nomic-ai/nomic-embed-text-v1.5-GGUF"
)
"""
embeding_instance = Embeding()

embeddings = embeding_instance.get_embedding(text=text)

print(f"embeddings {embeddings}")

modelo = 'TheBloke/Llama-2-7B-Chat-GGUF'
# modelo llm
llm = ChatOpenAI(
    base_url="http://localhost:1234/v1",
    model_name=modelo,
    temperature=0.0,
    openai_api_key="lm-studio"
)
# base de datos vectorial
db = chromadb.PersistentClient(path="./chroma_db_HF")
chroma_collection = db.get_or_create_collection("test_texto")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
# vectorstore = Chroma.from_documents(documents=fragmentos, embedding=embeddings)
# Creando index mejorado
svc = ServiceContext.from_defaults(embed_model=embeddings,llm=llm)
stc = StorageContext.from_defaults(vector_store=vector_store)

## Creando un nuevo index
index = VectorStoreIndex.from_documents(
    documentos, storage_context=stc, service_context=svc
)


query_engine = index.as_query_engine()
print("Terminada la creación del vectorstore")

# Crea la plantilla para el RAG (Retrieve and Generate)
plantilla = (
    "Dado el contexto que te proporcionare responde las preguntas \n"
    "Contexto:\n"
    "################################\n"
    "{context_str}"
    "################################\n"
    "Responde en español como si fueras un pirata: {query_str}\n"
)
qa_template = PromptTemplate(plantilla)
query_engine.update_prompts(
    {"response_synthesizer:text_qa_template": qa_template}
)

response = query_engine.query('Que tipo de animal es Leo y que tipo su amigo?')
print(f"respuesta: {response}")
