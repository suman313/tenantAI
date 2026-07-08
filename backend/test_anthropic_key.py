# test_anthropic_key.py
import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("❌ ANTHROPIC_API_KEY not found in .env file.")
    exit(1)

print(f"✅ Key loaded (starts with: {api_key[:12]}...)")

try:
    llm = ChatAnthropic(
        model="claude-opus-4-7", temperature=0, max_tokens=50  # your exact model
    )
    response = llm.invoke("Say 'Hello, your API key works!' in exactly that sentence.")
    print(f"✅ Claude response: {response.content}")
except Exception as e:
    print(f"❌ API call failed: {e}")
