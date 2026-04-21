import requests
from json import loads, dumps

# ---------------- SYSTEM PROMPT ---------------- #

SYSTEM_PROMPT = """
You are a coding assistant.

RULES:
1. Always respond in valid JSON.
2. Only ONE JSON object per response.
3. Keep it simple.

FORMAT:

{
  "type": "plan" | "action" | "final",
  "message": "string",
  "tool": {
    "name": "string",
    "input": "string"
  }
}

TOOLS:
get_weather(city: str)

EXAMPLE:

User: temperature of Mumbai

{
  "type": "action",
  "message": "Fetching weather for Mumbai",
  "tool": {
    "name": "get_weather",
    "input": "Mumbai"
  }
}

After tool:

{
  "type": "final",
  "message": "Temperature in Mumbai is 30°C"
}
"""

# ---------------- TOOL ---------------- #

def check_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=j1"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return f"{data['current_condition'][0]['temp_C']}°C"
    else:
        return "Error fetching weather"

# ---------------- OLLAMA CALL ---------------- #

def call_ollama(messages):
    url = "http://localhost:11434/api/generate"

    prompt = ""
    for m in messages:
        prompt += f"{m['role'].upper()}: {m['content']}\n"

    payload = {
        "model": "smallthinker:latest",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=payload)
    return response.json()["response"]

# ---------------- MAIN LOOP ---------------- #

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

user_input = input("Ask me anything 😁 >>> ")

message_history.append({
    "role": "user",
    "content": user_input
})

while True:
    raw_result = call_ollama(message_history)

    print("\nRAW:", raw_result)

    try:
        parsed = loads(raw_result)
    except:
        print("❌ Invalid JSON from model")
        break

    message_history.append({
        "role": "assistant",
        "content": raw_result
    })

    # ---------------- HANDLE TYPES ---------------- #

    if parsed["type"] == "plan":
        print("🧠", parsed["message"])

    elif parsed["type"] == "action":
        tool_name = parsed["tool"]["name"]
        tool_input = parsed["tool"]["input"]

        print(f"🔧 Calling tool: {tool_name}({tool_input})")

        if tool_name == "get_weather":
            result = check_weather(tool_input)

            # send tool result back
            tool_response = {
                "type": "plan",
                "message": f"Tool result: {result}"
            }

            message_history.append({
                "role": "assistant",
                "content": dumps(tool_response)
            })

    elif parsed["type"] == "final":
        print("\n✅ FINAL:", parsed["message"])
        break