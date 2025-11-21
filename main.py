import os
import google.generativeai as genai
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import markdown
from typing import List, Dict, Any

load_dotenv()
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Cấu hình Gemini (Dùng bản 1.5-flash ổn định)
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-2.5-flash')

chat_history: List[Dict[str, str]] = []

# API CHATBOT (Java gọi vào đây)
@app.post("/api/chat")
async def api_chat(request: Request):
    try:
        data = await request.json()
        # Tự động tìm 'message' (Java gửi) hoặc 'prompt'
        user_input = data.get("message") or data.get("prompt") or data.get("user_text")
        
        if not user_input:
            return {"error": f"Input not found. Java sent: {list(data.keys())}"}

        # Gọi Gemini
        response = model.generate_content(user_input)
        response_text = response.text
        
        # Trả về JSON đúng chuẩn Java cần
        return {
            "assistantResponse": response_text, 
            "text": response_text
        }
    except Exception as e:
        return {"error": str(e), "assistantResponse": f"AI Error: {str(e)}"}

# API GIẢ LẬP DICTATION (Để Java không lỗi 404)
@app.post("/api/v1/dictation/check")
async def check_dictation(request: Request):
    return {"score": 100, "diffs": [], "explanations": ["Mock Mode"]}

# WEB UI
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "chat_history": chat_history})