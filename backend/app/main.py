from fastapi import FastAPI
from pydantic import BaseModel
from app.ai_service import get_form_ai_suggestions
from fastapi.middleware.cors import CORSMiddleware

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