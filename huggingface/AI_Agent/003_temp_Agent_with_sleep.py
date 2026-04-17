from openai import OpenAI
from dotenv import load_dotenv
import requests
# load .env and call variable
import os
from json import dumps, loads


SYSTEM_PROMPT = '''
You are an expert in code. if user ask anything else just say sorry i cant do anything but code.

RULES : 
1) Strictly fallow the answer in json fromat
2) Only one step at a time
3) Follow chain of thought method to give me answer. 
4) for every tool_name step , wait for the output form api then give  "tool_action" step.



OUTPUT FORMAT:
{
    "step" : "start" | "plan" | "output" | "action" , "task" : { content" : "string" | "tool_name" : "string" , "input" : "string" | "tool_action" : "string" , "output" : "string"} 
}

AVAILABLE TOOLS :
1) get_weather(city :str) -> this function/tool takes city name and return the live temperature of city.   

Example 1 : 

Q : solve this : 2*5 + 10
A : 
{
    "step" : "START"  , "task" : {"content": "So you want to solve the given equation."}
    "step" : "PLAN"  , "task" : {"content": "we will use BODMAS system to do so "}
    "step" : "PLAN" , "task" :  {"content": "we will first multiply 2 with 5 thus we get 10"}
    "step" : "PLAN"  , "task" : {"content": "we will then add 10 into the 10 we got by multiplying 2 and 5, thus we get 20"}
    "step" : "OUTPUT" , "task" :  {"content": "thus the final answer is 20"   }
}

Example 2 : 
Q : what is temperatre of Pune city ?
A : 
{
    "step" : "START" ,"task": {"content": "I see , user wants to know the live temperature of Pune city."}
    "step" : "PLAN" ,"task" : {"content": "I have to check if there is any tool that can do this ?"}
    "step" : "PLAN" ,"task" : {"content": "We do have get_weather(city :str) tool available for this task }
    "step" : "PLAN" ,"task" : {"tool_name": "get_weather(city : str)", "input": "Pune" }
    "step" : "PLAN" ,"task" : {"tool_action" : "get_wethaer(city : str)","output" : "25 c" }
    "step" : "PLAN" ,"task" : {"content" : "Temperature of Pune is 25 C."}

 }   

 
Example 3 : 
Q : what is temperatre in Delhi?
A : 
{
    "step" : "START" ,"task": {"content": "I see , user wants to know the live temperature of Delhi city."}
    "step" : "PLAN" ,"task" : {"content": "I have to check if there is any tool that can do this ?"}
    "step" : "PLAN" ,"task" : {"content": "We do have get_weather(city :str) tool available for this task }
    "step" : "PLAN" ,"task" : {"tool_name": "get_weather(city : str)", "input": "Delhi" }
    "step" : "PLAN" ,"task" : {"tool_action" : "get_wethaer(city : str)","output" : "27 c" }
    "step" : "PLAN" ,"task" : {"content" : "Temperature of Delhi is 25 C."}

 }   



'''


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
        return f"Weather in {city} : {data["current_condition"][0]["temp_C"]}"
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
# print(check_weather("Mumbai"))

message_history = [
    {"role":"system","content":SYSTEM_PROMPT},
    ]

user_input = input("Ask me anything !!😁>>>")
message_history.append({
    "role": "user",
    "content":user_input
})

import time

import time
from json import loads

while True:
    try:
        response = client.chat.completions.create(
            model='gemini-2.5-flash',
            response_format={"type": "json_object"},
            messages=message_history
        )
    except Exception as e:
        print("⚠️ Rate limit hit, retrying...", e)
        time.sleep(7)
        continue

    raw_result = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": raw_result})

    # Parse JSON safely
    try:
        parsed_result = loads(raw_result)
    except Exception as e:
        print("❌ JSON parsing error:", e)
        break

    step = parsed_result.get("step")
    task = parsed_result.get("task", {})

    # ✅ FINAL OUTPUT
    if step == "OUTPUT":
        print("FINAL:", task.get("content"))
        break

    # ✅ NORMAL TEXT (PLAN / START)
    if "content" in task:
        print("🐮", task["content"])

    # ✅ TOOL CALL
    elif "tool_name" in task:
        tool_name = task.get("tool_name")
        city = task.get("input")

        print(f"🔧 Calling tool: {tool_name} with input: {city}")

        # call your function
        result = check_weather(city)

        print("🌤️", result)

        # send tool result back to LLM
        message_history.append({
            "role": "assistant",
            "content": result
        })

    # ✅ TOOL RESPONSE STEP (optional handling)
    elif "tool_action" in task:
        print("⚡ Tool returned:", task.get("output"))

    # small delay to avoid rate limit
    time.sleep(2)