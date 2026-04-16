from openai import OpenAI
from dotenv import load_dotenv
import requests
# load .env and call variable
import os

load_dotenv() #loads env variables from .env files like OPEN_AI_API variable
api_key = os.getenv("GEMINI_API_KEY")
client = OpenAI(
    api_key=api_key,  #api key is open
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

def check_weather(city : str):
    url = f"https://wttr.in/{city.lower()}?format=j1"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        return f"Weather  : {data["current_condition"][0]["temp_C"]}"
    else:
        return f"something went wrong, code : {response.status_code}"

def main():
    query = input("Query : ")
    response = client.chat.completions.create(
    model = "gemini-2.5-flash",
    messages = [
        {"role" : "user", "content" : query}
    ]
    )
    print(response.choices[0].message.content)

# main()
print(check_weather("pune"))