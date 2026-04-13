from ollama import Client
from fastapi import FastAPI,Body

# fast api object is craeted
app = FastAPI()

# create an ollama object
client = Client(
    host="http://localhost:11434",
)



@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
@app.post("/")
def chat(message: str = Body(...,description="this is message")) :
    response = client.chat(model="smallthinker:latest", messages=[
        {"role" : "user","content":message} 
    ])

    return {"response":response.message.content}