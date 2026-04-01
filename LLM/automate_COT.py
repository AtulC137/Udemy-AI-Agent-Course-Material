from openai import OpenAI
from dotenv import load_dotenv
from os import getenv
from json import dumps, loads
# import time

load_dotenv()

api_key = getenv('GEMINI_API_KEY')

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

SYSTEM_PROMPT = '''
You are an expert in code. if user ask anything else just say sorry i cant do anything but code.

RULES : 
1) Strictly fallow the answer in json fromat
2) Only one step at a time
3) Follow chain of thought method to give me answer. 


OUTPUT FORMAT:
{
    "step" : "start" | "plan" | "output" , "content" : "string"
}


Example : 

Q : solve this : 2*5 + 10
A : 
{
    "step" : "START" :"content": "So you want to solve the given equation."
    "step" : "PLAN" :"content": "we will use BODMAS system to do so "
    "step" : "PLAN" :"content": "we will first multiply 2 with 5 thus we get 10"
    "step" : "PLAN" :"content": "we will then add 10 into the 10 we got by multiplying 2 and 5, thus we get 20"
    "step" : "OUTPUT" :"content": "thus the final answer is 20"   
}


'''

message_history = [
    {"role":"system","content":SYSTEM_PROMPT},
    ]

user_input = input("Ask me anything !!😁>>>")
message_history.append({
    "role": "user",
    "content":user_input
})

while True:
    response = client.chat.completions.create(model='gemini-2.5-flash',
    response_format={"type" : "json_object"},
    messages=message_history)
    
    raw_result = response.choices[0].message.content
    message_history.append({"role" : "assistant", "content" : raw_result})

    parsed_result = loads(raw_result)
    if parsed_result.get("step")== "OUTPUT":
        print(parsed_result['content'])
        break
    print(parsed_result['content'],"🐮")
    # time.sleep(20)

