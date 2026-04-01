from openai import OpenAI
from dotenv import load_dotenv

load_dotenv() #loads env variables from .env files like OPEN_AI_API variable
client = OpenAI()

response = client.chat.completions.create(
    model = "gpt-4o-mini",
    messages = [
        {"role" : "user", "content" : "hey there ! who are you?"}
    ]
)

print(response.choices[0].message.content)
'''
This wont work as limite is excide, thus we use gemini api in Open ai setup
'''