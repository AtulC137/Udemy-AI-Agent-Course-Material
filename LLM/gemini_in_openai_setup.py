from openai import OpenAI
from dotenv import load_dotenv

# load .env and call variable
import os

load_dotenv() #loads env variables from .env files like OPEN_AI_API variable
api_key = os.getenv("GEMINI_API_KEY")
client = OpenAI(
    api_key=api_key,  #api key is open
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

response = client.chat.completions.create(
    model = "gemini-2.5-flash",
    messages = [
        {"role" : "user", "content" : "hey there ! who are you?"}
    ]
)

print(response.choices[0].message.content)
'''
This wont work as limite is excide, thus we use gemini api in Open ai setup
'''