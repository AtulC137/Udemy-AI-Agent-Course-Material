from openai import OpenAI
from dotenv import load_dotenv
from os import getenv

load_dotenv()

api_key = getenv('GEMINI_API_KEY')

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

SYSTEM_PROMPT = '''
You are an expert in code. if user ask anything else just say sorry i cant do anything but code.
**Strictly fallow the answer in json fromat**
OUTPUT FORMAT:
{
    "code" : "string" or NONE,
    "IsCodingQuestion" : boolean
}

Example : 
1) 
Q : write code for string reversal in python
A : 
{
    "code" : 
    '
    def rev(s):
        return s[::-1]
    ',
    "IsCodingQuestion" : True
}

2)
Q : write me a poem 
A : 
{
    "code" : None,
    "IsCodingQuestion" : False
}

'''
response = client.chat.completions.create(
    model='gemini-2.5-flash',
    messages=[
        {"role":"system","content":SYSTEM_PROMPT},
        # {"role":"user", "content": "how to solve tresendental equation?"},
        {"role":"user", "content": "code for palindroum"}
    ]
)

print(response.choices[0].message.content)