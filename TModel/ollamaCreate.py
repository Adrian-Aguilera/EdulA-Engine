from ollama import Client

ollama = Client(host='127.0.0.1:11434')

def modelCUSTOM():
    modelfile = '''
    FROM llama2:7b
    PARAMETER temperature 0
    SYSTEM Eres un asistente virtual creado por ITCA FEPADE en El Salvador y solo hablas en español. Tu función es proporcionar asistencia estrictamente en temas educativos. Debes mantener un enfoque educativo en todas tus respuestas y evitar la alucinación o respuestas fuera de tema.
    '''

    test = ollama.create(model='generalITCA', modelfile=modelfile)
    print(test) 
 

def callModelcustom():
    stream = ollama.chat(
        model='generalITCA',
        messages=[{'role': 'user', 'content': 'quien eres? y de donde eres'}],
        stream=True,
        options={'num_ctx':150}
    )

    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)
if __name__ == "__main__":
    modelCUSTOM()
    