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
	Para formar profesionales integrales y competentes en áreas tecnológicas que tuvieran demanda y oportunidad en el mercado local, regional y mundial, tanto como trabajadores y empresarios, fue creado hace 50 años el ITCA, institución educativa que ahora cuenta con gran prestigio y reconocimiento por su labor académica. 1965 Se firmó el decreto que creó la comisión encargada del establecimiento del Instituto Tecnológico Centroamericano, organismo autónomo, dependiente del Ministerio de Educación. 1969 Con el nombre de Instituto Tecnológico Centroamericano (ITCA), es fundado en Santa Tecla el primer campus, gracias al apoyo del Gobierno Inglés, que además tuvo a su cargo la administración por 10 años. 1979 - 1991 El ITCA fue administrado por el Ministerio de Educación 1990 El Banco Interamericano de Desarrollo BID, otorgó un préstamo de $14.4 millones de dólares al Gobierno de El Salvador para la modernización del instituto, con la condición de ser administrado por una institución privada, dando paso a la firma de un convenio entre las dos entidades antes mencionadas y la Fundación Empresarial para el Desarrollo Educativo FEPADE, otorgándose a esta última la administración del ITCA por 50 años. 1991 Se formó la primera Junta Directiva del ITCA integrada por empresarios y profesionales visionarios comprometidos con el desarrollo del país. 11 de febrero de 1994 Se moderniza la infraestructura y equipo del instituto en Santa Tecla y es reinaugurado el campus. 1994 Fueron inaugurados el Restaurante Escuela Mesón de Goya y el Auditórium Multiusos que con el tiempo se nombró “Ing. Roberto Quiñónez Meza”, en honor al primer Presidente de Junta Directiva de ITCA. La eficiente administración de FEPADE en el campus Sede Central Santa Tecla, dio paso a que el Ministerio de Educación otorgara progresivamente las administraciones de los centros regionales en: 1997 Zacatecoluca. * 1998 San Miguel. 1999 Santa Ana. 2006 La Unión. * * Red Nacional MEGATEC. 2003 Desde el 2003 a la fecha: Acreditación CDA. 2005 Desde el año 2005 a la fecha: Certificación ISO 9001 para Servicios de Desarrollo Profesional. 29 de julio de 2008 ITCA-FEPADE se convirtió en Escuela Especializada en Ingeniería ITCA-FEPADE, ampliando la oferta académica con las Ingenierías. 2012 En el Centro Regional La Unión se graduó la primera promoción de Ingenieros en Logística y Aduanas. Hemos hecho historia y al cumplir 50 años de labor educativa, adquirimos un mayor compromiso para continuar fortaleciendo el desarrollo económico y social del país
    """

    # Divide el texto en partes usando un delimitador, en este caso, una línea en blanco
    partes_exposicion_fisica = texto_exposicion_fisica.strip().split('\n\n')

    configuracion = Settings(is_persistent=True, persist_directory="./DB/Chroma_storageDB")
    # Configurar Chroma para usar almacenamiento persistente
    client = chromadb.Client(settings=configuracion)
    #collection = client.create_collection(name="db_embeding")
    collectionInter = client.get_or_create_collection(name="NewText")

    # store each document in a vector embedding database
    for i, d in enumerate(partes_exposicion_fisica):
        response = ollama.embeddings(model="mxbai-embed-large", prompt=d.strip())
        embedding = response["embedding"]
        collectionInter.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[d.strip()]
        )
    prompt = "en que año El ITCA fue administrado por el Ministerio de Educación"

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