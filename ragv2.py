from pathlib import Path

from langchain_community.llms import OpenAI
import chromadb

from langchain_openai import OpenAIEmbeddings

from langchain_core.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
#from langchain_community.embeddings import GPT4AllEmbeddings
from langchain import hub
from langchain_community.vectorstores import Chroma, FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

from embedings import Embeding

print("loading model")
client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

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

embeding_instance = Embeding()

embeddings = HuggingFaceBgeEmbeddings(configuration={"model": "nomic-ai/nomic-embed-text-v1.5-GGUF"})
new_client = chromadb.EphemeralClient()

vectorstore = Chroma.from_documents(documents=fragmentos, embedding=embeddings)
print("finished the vectorestore")
# Retrieve and generate using the relevant snippets of the blog.
retriever = vectorstore.as_retriever()
prompt = hub.pull("rlm/rag-prompt")
llm = client

template = """Use the provided pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Keep the answer as concise as possible.

CONTEXT:

```{context}```

QUESTION: {question}

HELPFUL ANSWER:"""
custom_rag_prompt = PromptTemplate.from_template(template)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def enter_question():
    print("about to invoke the rag_chain")
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | custom_rag_prompt
        | llm
        | StrOutputParser()
    )

    question = input("Enter your prompt: ")
    for chunk in rag_chain.stream(question):
        print(chunk, end="", flush=True)
    print("just finished invoking the rag_chain")
    # cleanup

while True:
    enter_question()

vectorstore.delete_collection()