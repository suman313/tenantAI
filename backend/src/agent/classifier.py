# src/agent/classifier.py
import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

load_dotenv()


class MaintenanceRequest(BaseModel):
    is_valid: bool = Field(
        description="True if this is a real tenant maintenance request, False if it's a newsletter, spam, bank alert, etc."
    )
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
    model = "openai/gpt-4o-mini"  # or "meta-llama/llama-4-maverick:free"

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
                """You are a property management assistant. Determine if the email is a genuine tenant maintenance request, then extract details.

- If the email is NOT a maintenance request (newsletter, advertisement, bank notification, system alert, etc.), set "is_valid": false and leave all other fields as their default values ("Other", "low", "unknown", "none", "none", "").
- If it IS a maintenance request, set "is_valid": true and extract the fields as follows:
  - issue_type: Plumbing / Electrical / HVAC / Appliance / Structural / Pest / Other
  - urgency: low / medium / high / emergency
  - unit_number: the apartment/unit number if mentioned, else "unknown"
  - tenant_phone: any phone number provided, else "none"
  - access_instructions: any access info, else "none"
  - summary: one sentence summary of the problem

Return ONLY valid JSON. No explanation, no markdown.""",
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
    # Ensure is_valid is always a bool
    data["is_valid"] = bool(data.get("is_valid", False))
    return MaintenanceRequest(**data)
