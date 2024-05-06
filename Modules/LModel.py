from openai import OpenAI
import threading
import time
import asyncio

class LModel():
    def __init__(self, api_key, model_point):
        self.client = OpenAI(base_url=model_point, api_key=api_key)
        self.animation_running = False

    def loading_animation(self):
        elementos = ['-', '\\', '|', '/']
        idx = 0
        while self.animation_running:
            print(elementos[idx % len(elementos)], end="\r")
            idx += 1
            time.sleep(0.1)
        print(" " * 20, end="\r")

    def chat(self, model, sys_content, user_question):
        messages = []
        print("Escribe 'salir' para terminar la conversación.")
        while True:
            if user_question.lower() == 'salir':
                break
            messages.append({"role": "system", "content": sys_content})
            messages.append({"role": "user", "content": user_question})

            self.animation_running = True
            animation_thread = threading.Thread(target=self.loading_animation)
            animation_thread.start()

            try:
                completion = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    stream=True, 
                    temperature=0.0,
                    max_tokens=150,
                )
            finally:    
                self.animation_running = False
                animation_thread.join()

            chat_response = completion.choices[0].message.content
            print("Assistant:", chat_response)
            messages.append({"role": "assistant", "content": chat_response})
            
    async def response_chat(self, model, sys_content, message_user):
        histoy_conversation = []
        histoy_conversation.append({"role": "system", "content": sys_content})
        histoy_conversation.append({"role": "user", "content": message_user})
        try:
            completion = self.client.chat.completions.create(
                model=model,
                messages=histoy_conversation,
                #stream=True, 
                temperature=0,
                max_tokens=50,
            )
            message_return = completion.choices[0].message.content
            print(f"data: {completion}")
            return ({
                "response": message_return
            })
        except Exception as e:
            return ({
                "error_model":f"{str(e)}"
            })
            
    async def av_chat(self, mode, system_content, message_user):
        
        return message_user