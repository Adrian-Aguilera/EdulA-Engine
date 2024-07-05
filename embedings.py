from openai import OpenAI

class Embeding():
    def __init__(self):
        self.client =  OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    def get_embedding(self, text, model="nomic-ai/nomic-embed-text-v1.5-GGUF"):
        text = text.replace("\n", " ")
        return self.client.embeddings.create(input = [text], model=model).data[0].embedding