import requests

json = {
    "modelo": "llama2:7b ",
    "mensaje" : {
        "role": "user",
        "content":"como estas"
    }
}
response = requests.post("https://3fd9d8732313a4510f2b3d25f5d136a2.serveo.net/LLMS/Model/ollmaClient", json=json)

responsetext = response.text
print(responsetext)