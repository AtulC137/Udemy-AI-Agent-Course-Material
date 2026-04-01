from dotenv import load_dotenv
from google import genai
import os

load_dotenv() #loads env variables from .env files like OPEN_AI_API variable

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(
    api_key=api_key
)

response = client.models.generate_content(
    model = "gemini-2.5-flash",
    contents="hii! who are you?"
)

print(response.text)
'''
this is how we use gemini
'''
