from openai import OpenAI
from dotenv import load_dotenv
from os import getenv

load_dotenv()

api_key = getenv('GEMINI_API_KEY')

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

SYSTEM_PROMPT = "You are an expert in math. if user ask anything else just say sorry i cant do anything but math"
response = client.chat.completions.create(
    model='gemini-2.5-flash',
    messages=[
        {"role":"system","content":SYSTEM_PROMPT},
        {"role":"user", "content": "how to solve tresendental equation?"}
    ]
)

print(response.choices[0].message.content)