import requests

url = "http://localhost:11434/api/generate"

payload = {
    "model": "smallthinker:latest",
    "prompt": "hey there! who are you?",
    "stream": False
}

response = requests.post(url, json=payload)

data = response.json()
print(data["response"])