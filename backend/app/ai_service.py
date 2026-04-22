import os
import json
from dotenv import load_dotenv
from openai import AsyncOpenAI
from typing import List, Dict

# -----------------------------
# LOAD ENV
# -----------------------------
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))

# -----------------------------
# ENV CONFIG
# -----------------------------
DEV_KEY = os.getenv("dev_key")
CLINE_BASE_URL = os.getenv("CLINE_BASE_URL", "https://api.cline.bot/api/v1")
CLINE_MODEL = os.getenv("CLINE_MODEL", "openai/gpt-4o-mini")

if not DEV_KEY:
    raise ValueError("Missing dev_key in .env")

# -----------------------------
# AI CLIENT
# -----------------------------
client = AsyncOpenAI(
    base_url=CLINE_BASE_URL,
    api_key=DEV_KEY,
)

# -----------------------------
# GENERIC CHAT FUNCTION
# -----------------------------
async def get_ai_response(messages: List[Dict[str, str]]) -> dict:
    try:
        response = await client.chat.completions.create(
            model=CLINE_MODEL,
            messages=messages,
            temperature=0.5
        )

        content = None

        # OpenAI format
        if hasattr(response, "choices") and response.choices:
            content = response.choices[0].message.content

        # Cline format
        if not content and hasattr(response, "data"):
            content = response.data["choices"][0]["message"]["content"]

        if not content:
            print("FULL RESPONSE DEBUG:", response)
            content = "AI returned empty response"

        return {
            "role": "assistant",
            "content": content
        }

    except Exception as e:
        print("AI ERROR:", e)
        return {
            "role": "assistant",
            "content": str(e),
            "error": True
        }

# -----------------------------
# RESUME AI FUNCTION 🔥
# -----------------------------
async def get_form_ai_suggestions(form_data: dict) -> dict:

    prompt = f"""
You are an AI Resume Assistant.

User is building a professional resume.

Input:
{form_data}

Tasks:
1. Improve writing professionally
2. Fix grammar
3. Make it job-ready

STRICT RULE:
Return ONLY valid JSON

Format:
{{
  "errors": {{}},
  "suggestions": {{}},
  "autoFill": {{}}
}}

IMPORTANT:
- suggestions = explain improvement
- autoFill = improved version
"""

    messages = [
        {"role": "system", "content": "You only return JSON."},
        {"role": "user", "content": prompt}
    ]

    response = await get_ai_response(messages)
    content = response.get("content", "")

    try:
        # remove markdown if exists
        if "```" in content:
            content = content.split("```")[1]
            content = content.replace("json", "").strip()

        return json.loads(content)

    except Exception as e:
        print("JSON ERROR:", e)
        print("RAW:", content)

        return {
            "errors": {},
            "suggestions": {},
            "autoFill": {},
            "raw": content
        }