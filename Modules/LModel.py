from openai import OpenAI
import threading
import time
import asyncio

class LModel():
    def __init__(self, api_key, model_point):
        self.client = OpenAI(base_url=model_point, api_key=api_key)
        
    async def av_chat(self, mode, system_content, message_user):
        
        return message_user
    
    async def response_general(self, mode, system_content, message_user):
        return message_user