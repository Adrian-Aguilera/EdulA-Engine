# Make sure to `pip install openai` first
from openai import OpenAI
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

def get_embedding(text, model="nomic-ai/nomic-embed-text-v1.5-GGUF"):
   text = text.replace("\n", " ")
   print(text)
   return client.embeddings.create(input = [text], model=model).data[0].embedding

print(get_embedding("itca fepade"))