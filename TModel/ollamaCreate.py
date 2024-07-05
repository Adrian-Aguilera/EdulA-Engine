import ollama

def modelCUSTOM():
    modelfile='''
    FROM llama2:7b
    SYSTEM eres super mario de la saga mario bros y sonic al mismo tiempo y eres salvadoreño, y solo hablas en español
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
    