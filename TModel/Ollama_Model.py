import ollama

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