from openai import OpenAI
import threading
import time

client = OpenAI(base_url="https://42b6-190-62-84-58.ngrok-free.app/v1", api_key="lm-studio")

def loading_animation():
    global animation_running
    elementos = ['-', '\\', '|', '/']
    idx = 0
    while animation_running:
        print(elementos[idx % len(elementos)], end="\r")
        idx += 1
        time.sleep(0.1)
    print(" "*20, end="\r")
    
animation_running = False
def chat():
    global animation_running
    messages = []  # Lista para almacenar el historial de mensajes
    
    print("Escribe 'salir' para terminar la conversación.")
    
    while True:
        user_input = input("Tú: ")
        if user_input.lower() == 'salir':
            break
        messages.append({"role": "system", "content": "eres un tutor digital diseñado por la institucion ITCA fepade de el salvador, ayudas a los estudiantes en cualquier duda, y solo hablas español!"})

        messages.append({"role": "user", "content": user_input})

        animation_running = True
        animation_thread = threading.Thread(target=loading_animation)
        animation_thread.start()
        
        completion = client.chat.completions.create(
            model="TheBloke/Llama-2-7B-Chat-GGUF/llama-2-7b-chat.Q2_K.gguf",
            messages=messages,
            temperature=0.4,
            max_tokens=150,
        )

        animation_running = False
        animation_thread.join()

        chat_response = completion.choices[0].message.content
        print("ChatGPT:", chat_response)
        
        messages.append({"role": "assistant", "content": chat_response})

if __name__ == "__main__":
    chat()