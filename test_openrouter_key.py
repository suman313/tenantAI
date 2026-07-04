# test_openrouter_key.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    print("❌ OPENROUTER_API_KEY not found in .env")
    exit(1)

print(f"✅ Key loaded: {api_key[:15]}...")

# Use a fast, free model for testing
model = "nvidia/nemotron-3-ultra-550b-a55b:free"  # free on OpenRouter

try:
    llm = ChatOpenAI(
        model=model,
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        temperature=0,
        max_tokens=50,
        # Optional: include HTTP-Referer and X-Title for ranking
        # default_headers={"HTTP-Referer": "http://localhost", "X-Title": "PropertyAI"}
    )
    response = llm.invoke("Say 'Hello, OpenRouter works!' exactly.")
    print(f"✅ Response: {response.content}")
except Exception as e:
    print(f"❌ API call failed: {e}")
