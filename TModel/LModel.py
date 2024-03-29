# Example: reuse your existing OpenAI setup
from openai import OpenAI

"""
# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

completion = client.chat.completions.create(
  model="TheBloke/Llama-2-7B-Chat-GGUF/llama-2-7b-chat.Q2_K.gguf",
  messages=[
    {"role": "system", "content": "Eres un asistene virtual"},
    {"role": "user", "content": "hola me llamo adrian"}
  ],
  temperature=0.7,
)

print(completion.choices[0].message.content)
"""

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

def chat():
    messages = []  # Lista para almacenar el historial de mensajes
    
    print("Escribe 'salir' para terminar la conversación.")
    
    while True:
        user_input = input("Tú: ")
        if user_input.lower() == 'salir':
            break
        messages.append({"role": "system", "content": "Eres un asistente virtual que solo habla español"})

        messages.append({"role": "user", "content": user_input})

        
        completion = client.chat.completions.create(
            model="TheBloke/Llama-2-7B-Chat-GGUF/llama-2-7b-chat.Q2_K.gguf",
            messages=messages,
            temperature=0.7,
        )

        
        chat_response = completion.choices[0].message.content
        print("ChatGPT:", chat_response)
        
        # Añade la respuesta al historial de mensajes
        messages.append({"role": "assistant", "content": chat_response})

if __name__ == "__main__":
    chat()