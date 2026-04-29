import requests
import json

# =========================
# SYSTEM PROMPT
# =========================
SYSTEM_PROMPT = """
You are a JSON-only coding agent.

RULES:
1) Always respond in STRICT JSON
2) Only ONE step per response
3) Do NOT explain anything
4) Follow step flow: START → PLAN → ACTION → OUTPUT
5) When calling tools:
   - First ACTION with input
   - Then wait for output

FORMAT:
{
  "step": "START" | "PLAN" | "ACTION" | "OUTPUT",
  "task": {
    "content": "string",
    "tool": "string",
    "input": "string",
    "output": "string"
  }
}

TOOLS:
- get_weather(city)
"""

# =========================
# TOOL
# =========================
def check_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=j1"
    r = requests.get(url)
    data = r.json()
    return f"{data['current_condition'][0]['temp_C']} °C"


# =========================
# OLLAMA CHAT CALL (IMPORTANT)
# =========================
def call_ollama_chat(messages):
    url = "http://localhost:11434/api/chat"

    payload = {
        "model": "smallthinker:latest",
        "messages": messages,
        "stream": False,
        "format": "json"   # 🔥 THIS IS KEY (like OpenAI JSON mode)
    }

    response = requests.post(url, json=payload)
    data = response.json()

    return data["message"]["content"]


# =========================
# MAIN
# =========================
message_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

user_input = input("Ask me anything 😁 >>> ")
message_history.append({
    "role": "user",
    "content": user_input
})


# =========================
# LOOP (same as your working version)
# =========================
while True:
    raw_result = call_ollama_chat(message_history)

    # skip empty responses
    if not raw_result.strip() or raw_result.strip() == "{}":
        continue

    # append response
    message_history.append({
        "role": "assistant",
        "content": raw_result
    })

    # parse JSON
    try:
        parsed = json.loads(raw_result)
    except:
        continue  # skip bad responses instead of breaking

    step = parsed.get("step")
    task = parsed.get("task", {})
    content = task.get("content", "")

    # =========================
    # CLEAN PRINTS
    # =========================
    if step == "START":
        print(f"\n🚀 START: {content}")

    elif step == "PLAN":
        print(f"🧠 PLAN: {content}")

    elif step == "ACTION":
        tool = task.get("tool")
        tool_input = task.get("input")

        # tool call
        if tool == "get_weather" and tool_input:
            result = check_weather(tool_input)

            print(f"🔧 ACTION: calling {tool}({tool_input})")
            print(f"🌡️ RESULT: {result}")

            tool_response = {
                "role": "assistant",
                "content": json.dumps({
                    "step": "ACTION",
                    "task": {
                        "tool": "get_weather",
                        "output": result
                    }
                })
            }

            message_history.append(tool_response)
            continue

    elif step == "OUTPUT":
        print(f"\n✅ FINAL: {content}")
        break