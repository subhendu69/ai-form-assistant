from fastapi import FastAPI
from pydantic import BaseModel
from app.ai_service import get_form_ai_suggestions

app = FastAPI()


class FormData(BaseModel):
    name: str | None = None
    age: str | None = None
    email: str | None = None
    job: str | None = None


@app.post("/form-ai")
async def form_ai(data: FormData):
    return await get_form_ai_suggestions(data.dict())