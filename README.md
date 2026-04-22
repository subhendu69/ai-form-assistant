Smart Form Validation using AI (Python + Angular)

An end-to-end full-stack application that uses AI to validate, correct, and guide user inputs in real time, reducing form errors and improving user experience.

💡 Designed to demonstrate AI integration + scalable architecture + frontend-backend communication

🔥 Why This Project Stands Out

Most forms only validate syntax.
This project goes further by using AI to: 

Understand contextual mistakes (not just empty fields)
Suggest human-like corrections
Provide intelligent feedback instead of rigid rules

👉 Example:
Instead of just saying "Invalid email", it suggests:
"Did you mean example@gmail.com
?"

🧠 Key Highlights
⚡ Real-time AI validation
🧩 Clean separation of frontend & backend
🔌 RESTful API design
🧠 AI prompt engineering for structured JSON output
📉 Reduces user error rate significantly (practical UX impact)
🏗️ Architecture Overview
[ Angular Frontend ]
        ↓
 REST API (HTTP)
        ↓
[ Python Backend (FastAPI) ]
        ↓
[ AI Model Service ]
        ↓
 Structured JSON Response
🛠️ Tech Stack
Layer	Technology
Frontend	Angular, TypeScript
Backend	Python, FastAPI
AI Layer	OpenAI API / LLM
Communication	REST API (JSON)
⚙️ Setup & Run Locally
🔹 Backend
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
🔹 Frontend
cd frontend
npm install
ng serve
🔌 API Example
Request
{
  "message": {
    "name": "John",
    "age": "",
    "email": "john@@gmail"
  }
}
Response
{
  "errors": {
    "age": "Age cannot be empty",
    "email": "Invalid email format"
  },
  "suggestions": {
    "email": "Try: john@gmail.com"
  }
}
🎯 What I Learned
This project demonstrates:

✅ Full-stack development skills
✅ Real-world AI integration
✅ Clean architecture & scalability thinking
✅ Problem-solving & debugging ability
