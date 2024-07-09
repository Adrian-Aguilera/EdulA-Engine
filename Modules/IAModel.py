from openai import OpenAI
import ollama
from dotenv import load_dotenv
import os
import chromadb
from chromadb.config import Settings

load_dotenv()
class LModel:
    def __init__(self, api_key=None, model_point=None):
        #self.client = OpenAI(base_url=model_point, api_key=api_key)
        self.modelo = os.environ.get("MODELLM")
        self.modelEmbedding= os.environ.get("MODELEMBEDDING")
        self.is_persistent = os.environ.get("IS_PERSISTENT", "False").lower() in ("true", '1', 't')
        self.persist_directory = os.environ.get("PERSIST_DIRECTORY")
        self.systemContent = os.environ.get("SYS_CONTENT")
        #client Chroma para que que cree la db se guarde
        self.ChromaClient = chromadb.Client(
            settings=Settings(
                is_persistent=self.is_persistent,
                persist_directory=self.persist_directory
            )
        )


    async def av_chat(self, mode, system_content, message_user):
        return message_user

    #Funcion principal
    async def responseGeneral(self, message_user):
        try:
            nameCollection = 'Tcollection'
            userEmbeddings = await self._responseEmbedding(message_user, nameCollection=nameCollection)
            response = await self._callGenerate(message_user, contextEmbedding=userEmbeddings)
            if response:
                return {"message": response}
        except Exception as e:
            return {"error": "Error al conectar la motor"}

    async def _callGenerate(self, message_user, contextEmbedding):
        output = []
        responseCall = await ollama.generate(
            model=self.modelo,
            prompt=f"{self.systemContent}{contextEmbedding}. Responde a este mensaje: {message_user}",
            stream=True,
        )
        for fragmento in responseCall:
            output.append(fragmento["response"], end="", flush=True)

        return  ''.join(output)

    async def _callEmbeding(self,promt):
        try:
            reponseEmbeddings = await ollama.embeddings(
                prompt=promt,
                model=self.modelEmbedding
            )
            return reponseEmbeddings
        except Exception as e:
            return str(e)

    #funcion para guardar una coleccion para almacenar el contexto del los datos
    async def _embeddingsDataBase(self, nameCollection, dataContext):
        try:
            operacion = True
            Collection= self.ChromaClient.get_or_create_collection(name=nameCollection)
            for i, d in enumerate(dataContext):
                try:
                    response = await self._callEmbeding(model=self.modelEmbedding, prompt=d)
                    embedding = response["embedding"]
                    Collection.add(
                        ids=[str(i)],
                        embeddings=[embedding],
                        documents=[d]
                    )
                except Exception as e:
                    operacion = False
            return operacion
        except Exception as e:
            return {"Expetion": f'Error al obtener Embeddig Database: {str(e)}'}

    async def _responseEmbedding(self, userMessage, nameCollection):
        try:
            userMessageEmbedding = await self._callEmbeding(promt=userMessage)
            Collection= self.ChromaClient.get_or_create_collection(name=nameCollection)
            results = Collection.query(
                query_embeddings=[userMessageEmbedding["embedding"]],
                n_results=1
            )
            respuesta = results['documents'][0][0]
            return respuesta
        except Exception as e:
            return
