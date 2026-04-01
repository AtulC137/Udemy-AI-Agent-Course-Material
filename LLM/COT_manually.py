from openai import OpenAI
from dotenv import load_dotenv
from os import getenv
from json import dumps

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
    "step" : "START" : "So you want to solve the given equation."
    "step" : "PLAN" : "we will use BODMAS system to do so "
    "step" : "PLAN" : "we will first multiply 2 with 5 thus we get 10"
    "step" : "PLAN" : "we will then add 10 into the 10 we got by multiplying 2 and 5, thus we get 20"
    "step" : "OUTPUT" : "thus the final answer is 20"   
}


'''
response = client.chat.completions.create(
    model='gemini-2.5-flash',
    response_format={"type" : "json_object"},
    messages=[
        {"role":"system","content":SYSTEM_PROMPT},
        # {"role":"user", "content": "how to solve tresendental equation?"},
        # Initially we will have only this message !!!
        {"role":"user", "content": "solve 2*10*3+2"},

        # append the output of the llm to the message in string not in json
        {"role":"assistant", "content" : dumps({
            "step": "start",
            "content": "So you want to solve the given equation: 2*10*3+2."
        })},

        # append the output of llm to message again
        {"role":"assistant", "content" : dumps({
            "step": "plan",
            "content": "We will use the order of operations (BODMAS/PEMDAS) to solve this problem. This means we perform multiplication before addition."
        })},

        # qppend next
        {"role":"assistant", "content" : dumps({
            "step": "plan",
            "content": "First, we will perform the multiplications from left to right."
        })},

        # append next 
         {"role":"assistant", "content" : dumps({
            "step": "plan",
            "content": "First, multiply 2 by 10, which gives 20."
        })},
    ]
)

print(response.choices[0].message.content)