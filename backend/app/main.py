from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AI Form Assistant")


# -----------------------------
# Request Model
# -----------------------------
class FormData(BaseModel):
    name: str | None = None
    age: str | None = None
    email: str | None = None
    job: str | None = None


# -----------------------------
# Health Check
# -----------------------------
@app.get("/")
def home():
    return {
        "message": "AI Form Assistant backend is running"
    }


# -----------------------------
# Form AI Endpoint (base version)
# -----------------------------
@app.post("/form-ai")
def form_ai(data: FormData):

    errors = {}
    suggestions = {}
    auto_fill = {}

    # Email validation
    if data.email:
        if "@" not in data.email or "." not in data.email:
            errors["email"] = "Invalid email format"

    # Age suggestion
    if not data.age:
        suggestions["age"] = "Suggested range: 22 - 35"

    # Job enrichment
    if data.job:
        if "frontend" in data.job.lower():
            auto_fill["job"] = "Frontend Developer (Angular)"
        elif "backend" in data.job.lower():
            auto_fill["job"] = "Backend Developer (FastAPI)"

    return {
        "errors": errors,
        "suggestions": suggestions,
        "autoFill": auto_fill
    }