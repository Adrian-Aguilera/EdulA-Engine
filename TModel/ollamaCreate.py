from ollama import Client

ollama = Client(host='127.0.0.1:11434')
def modelCUSTOM():
    modelfile='''
    FROM llama2:7b
    SYSTEM eres un asistente virtual hecho por la ITCA FEPADE, y solo hablas en español
    '''

    test = ollama.create(model='prueba', modelfile=modelfile)
    print(test)  

def callModelcustom():
    stream = ollama.chat(
        model='prueba',
        messages=[{'role': 'user', 'content': 'quien eres? y de donde eres'}],
        stream=True,
    )

    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)
if __name__ == "__main__":
    callModelcustom()
    