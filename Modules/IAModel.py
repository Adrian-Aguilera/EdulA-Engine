from openai import OpenAI
import ollama
from dotenv import load_dotenv
import os
import chromadb
from chromadb.config import Settings
from asgiref.sync import async_to_sync

load_dotenv()


class GeneralModel:
    def __init__(self, api_key=None, model_point=None):
        self.MODELLM = os.environ.get("MODELLM")
        self.modelEmbedding = os.environ.get("MODELEMBEDDING")
        self.is_persistent = os.environ.get("IS_PERSISTENT", "False").lower() in ("true", '1', 't')
        self.persist_directory = os.environ.get("PERSIST_DIRECTORY")
        self.systemContent = os.environ.get("SYS_CONTENT")
        # client Chroma para que cree la db y se guarde
        self.ChromaClient = chromadb.Client(
            settings=Settings(
                is_persistent=self.is_persistent,
                persist_directory=self.persist_directory,
            )
        )
        self.ollamaClient = ollama.AsyncClient(host=os.environ.get("OLLAMACLIENT"))

    # funcion principal de general response
    async def responseGeneral(self, message_user):
        try:
            nameCollection = "Tcollection"
            userEmbeddings = await self._responseEmbedding(
                message_user, nameCollection=nameCollection
            )
            responseGenerate = await self._callGenerate(
                message_user=message_user, contextEmbedding=userEmbeddings
            )
            print(responseGenerate)
            return responseGenerate
        except Exception as e:
            return {"error": f"Error al conectar con el motor: {str(e)}"}

    async def _callGenerate(self, message_user, contextEmbedding=None):
        try:
            responseCall = await self.ollamaClient.chat(
                model=self.MODELLM,
                prompt=f"{self.systemContent}{contextEmbedding}. Responde a este mensaje: {message_user}",
                stream=False,
                options={'num_ctx': 150}
            )
            # print(responseCall["response"])
            return {"message": f'{responseCall["response"]}'}
        except Exception as e:
            return {"error": f"Error en la generación de respuesta: {str(e)}"}

    async def _callEmbedding(self, prompt):
        try:
            responseEmbeddings = await self.ollamaClient.embeddings(
                prompt=prompt, model=self.modelEmbedding
            )
            return responseEmbeddings
        except Exception as e:
            return {"error": f"Error en la obtención de embeddings: {str(e)}"}

    def _embeddingsDataBase(self, nameCollection, dataContext):
        try:
            operacion = True
            Collection = self.ChromaClient.get_or_create_collection(name=nameCollection)
            for i, d in enumerate(dataContext):
                try:
                    response = async_to_sync(self._callEmbedding)(prompt=d)
                    embedding = response["embedding"]
                    Collection.add(ids=[str(i)], embeddings=[embedding], documents=[d])
                except Exception as e:
                    print(f"Error al agregar el documento {d}: {str(e)}")
                    operacion = False
            return operacion
        except Exception as e:
            return {"Exception": f"Error al obtener Embedding Database: {str(e)}"}

    async def _responseEmbedding(self, userMessage, nameCollection):
        try:
            userMessageEmbedding = await self._callEmbedding(prompt=userMessage)
            Collection = self.ChromaClient.get_collection(name=nameCollection)
            results = Collection.query(
                query_embeddings=[userMessageEmbedding["embedding"]], n_results=1
            )
            respuesta = results["documents"][0][0]
            print(respuesta)
            return respuesta
        except Exception as e:
            return {"error": f"Error en la respuesta de embedding: {str(e)}"}
