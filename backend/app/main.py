from fastapi import FastAPI
from pydantic import BaseModel
from app.ai_service import get_form_ai_suggestions
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class FormData(BaseModel):
    name: str | None = None
    age: str | None = None
    email: str | None = None
    job: str | None = None


@app.post("/form-ai")
async def form_ai(data: FormData):
    return await get_form_ai_suggestions(data.dict())
@app.post("/generate-resume")
async def generate_resume(data: dict):
    file_path = "resume.pdf"

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    content = []

    # Title
    content.append(Paragraph("<b>Resume</b>", styles["Title"]))
    content.append(Spacer(1, 10))

    # Role
    content.append(Paragraph(f"<b>Role:</b> {data.get('role', '')}", styles["Normal"]))
    content.append(Spacer(1, 10))

    # Skills
    content.append(Paragraph("<b>Skills:</b>", styles["Heading3"]))
    content.append(Paragraph(data.get("skills", ""), styles["Normal"]))
    content.append(Spacer(1, 10))

    # Experience
    content.append(Paragraph("<b>Experience:</b>", styles["Heading3"]))
    content.append(Paragraph(data.get("experience", ""), styles["Normal"]))
    content.append(Spacer(1, 10))

    # Summary
    content.append(Paragraph("<b>Summary:</b>", styles["Heading3"]))
    content.append(Paragraph(data.get("summary", ""), styles["Normal"]))

    doc.build(content)

    return FileResponse(file_path, media_type='application/pdf', filename="resume.pdf")