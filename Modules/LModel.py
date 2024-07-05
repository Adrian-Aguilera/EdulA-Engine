from openai import OpenAI
import threading
import time
import asyncio

class LModel():
    def __init__(self, api_key, model_point):
        self.client = OpenAI(base_url=model_point, api_key=api_key)
    
    
    async def response_chat(self, model, sys_content, message_user, mode):
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