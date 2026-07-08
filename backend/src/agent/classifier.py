# src/agent/classifier.py
import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

load_dotenv()


class MaintenanceRequest(BaseModel):
    issue_type: str = Field(
        description="Plumbing, Electrical, HVAC, Appliance, Structural, Pest, Other"
    )
    urgency: str = Field(description="low, medium, high, emergency")
    unit_number: str = Field(default="unknown")
    tenant_phone: str = Field(default="none")
    access_instructions: str = Field(default="none")
    summary: str = Field(description="One-sentence summary")


def classify_email(email_body: str) -> MaintenanceRequest:
    # Use a free/cheap model; change to paid ones for production
    model = "nvidia/nemotron-3-ultra-550b-a55b:free"  # or "meta-llama/llama-4-maverick:free"

    llm = ChatOpenAI(
        model=model,
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
        temperature=0,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You extract structured maintenance request data from tenant emails.
Return ONLY a valid JSON object with these keys:
- issue_type (one of: Plumbing, Electrical, HVAC, Appliance, Structural, Pest, Other)
- urgency (one of: low, medium, high, emergency)
- unit_number (string, or "unknown")
- tenant_phone (string, or "none")
- access_instructions (string, or "none")
- summary (one sentence)

If a field is missing, use the defaults: "unknown", "none", "none".
No explanations, no markdown, just the JSON object.""",
            ),
            ("human", "{email_body}"),
        ]
    )

    chain = prompt | llm
    raw = chain.invoke({"email_body": email_body})
    content = raw.content.strip()

    # Clean up markdown code fences if present
    if content.startswith("```"):
        content = content.split("\n", 1)[1]
        if content.endswith("```"):
            content = content[:-3]

    data = json.loads(content)
    return MaintenanceRequest(**data)
