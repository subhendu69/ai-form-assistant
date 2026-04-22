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

print("ENV CHECK -> dev_key:", "FOUND" if DEV_KEY else "MISSING")

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
# GENERIC CHAT FUNCTION (FINAL FIX 🔥)
# -----------------------------
async def get_ai_response(messages: List[Dict[str, str]]) -> dict:
    try:
        formatted_messages = [
            {
                "role": msg.get("role", "user") if isinstance(msg, dict) else getattr(msg, "role", "user"),
                "content": msg.get("content", "") if isinstance(msg, dict) else getattr(msg, "content", "")
            }
            for msg in messages
        ]

        response = await client.chat.completions.create(
            model=CLINE_MODEL,
            messages=formatted_messages,
            temperature=0.3
        )

        content = None

        # ✅ CASE 1: Standard OpenAI format
        try:
            if hasattr(response, "choices") and response.choices:
                content = response.choices[0].message.content
        except Exception:
            pass

        # ✅ CASE 2: Cline format (IMPORTANT 🔥)
        if not content:
            try:
                if hasattr(response, "data") and response.data:
                    content = response.data["choices"][0]["message"]["content"]
            except Exception:
                pass

        # ❌ DO NOT stringify full response

        # ✅ FINAL fallback
        if not content:
            print("FULL RESPONSE DEBUG:", response)
            content = "AI returned empty response"

        return {
            "role": "assistant",
            "content": content
        }

    except Exception as e:
        print("AI ERROR:", repr(e))
        return {
            "role": "assistant",
            "content": f"Backend error: {str(e)}",
            "error": True
        }


# -----------------------------
# FORM AI FUNCTION (FINAL 🔥)
# -----------------------------
async def get_form_ai_suggestions(form_data: dict) -> dict:

    prompt = f"""
You are an AI Form Assistant.

Analyze this form data:
{form_data}

Tasks:
1. Validate fields
2. Suggest missing values
3. Improve values

STRICT RULE:
Return ONLY valid JSON.

Format:
{{
  "errors": {{}},
  "suggestions": {{}},
  "autoFill": {{}}
}}
"""

    messages = [
        {"role": "system", "content": "You only return JSON."},
        {"role": "user", "content": prompt}
    ]

    response = await get_ai_response(messages)
    content = response.get("content", "")

    # -----------------------------
    # CLEAN + PARSE JSON
    # -----------------------------
    try:
        content = content.strip()

        # remove markdown if exists
        if "```" in content:
            content = content.split("```")[1]
            content = content.replace("json", "").strip()

        parsed = json.loads(content)

        return parsed

    except Exception as e:
        print("JSON PARSE ERROR:", e)
        print("RAW AI:", content)

        return {
            "errors": {},
            "suggestions": {},
            "autoFill": {},
            "raw": content
        }