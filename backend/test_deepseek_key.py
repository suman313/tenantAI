# test_deepseek_key.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI  # ← changed

load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")  # ← changed
if not api_key:
    print("❌ DEEPSEEK_API_KEY not found in .env file.")
    exit(1)

print(f"✅ Key loaded (starts with: {api_key[:12]}...)")

try:
    llm = ChatOpenAI(  # ← changed
        model="deepseek-chat",  # ← changed
        api_key=api_key,
        base_url="https://api.deepseek.com/v1",  # ← added
        temperature=0,
        max_tokens=50,
    )
    response = llm.invoke("Say 'Hello, your API key works!' in exactly that sentence.")
    print(f"✅ DeepSeek response: {response.content}")
except Exception as e:
    print(f"❌ API call failed: {e}")
