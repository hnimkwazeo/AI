import os
import google.generativeai as genai
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from pydantic import BaseModel
import tempfile
import speech_recognition as sr
from gtts import gTTS
import base64
from pydub import AudioSegment  # <-- Import mới

load_dotenv()
app = FastAPI()

api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-2.5-flash')

class ChatRequest(BaseModel):
    message: str

class TTSRequest(BaseModel):
    text: str

@app.post("/api/chat")
async def api_chat(request: ChatRequest):
    try:
        response = model.generate_content(request.message)
        return {"text": response.text}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/transcribe")
async def transcribe_audio(audio: UploadFile = File(...)):
    temp_filename = "temp_audio_input" 
    wav_filename = "temp_audio_converted.wav" 
    
    try:
        audio_data = await audio.read()
        
      
        with open(temp_filename, "wb") as f:
            f.write(audio_data)
        

        sound = AudioSegment.from_file(temp_filename)
        sound.export(wav_filename, format="wav")
        
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_filename) as source:
            audio_content = recognizer.record(source)
        
        try:
            text = recognizer.recognize_google(audio_content, language='vi-VN')
        except sr.UnknownValueError:
            try:
                text = recognizer.recognize_google(audio_content, language='en-US')
            except sr.UnknownValueError:
                return JSONResponse(content={"error": "Không nghe rõ, vui lòng nói lại."}, status_code=400)
        
        return {"text": text}
        
    except Exception as e:
        print(f"Lỗi Transcribe: {e}")
        return JSONResponse(content={"error": f"Lỗi xử lý audio: {str(e)}"}, status_code=500)
        
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        if os.path.exists(wav_filename):
            os.remove(wav_filename)

@app.post("/text-to-speech")
async def text_to_speech(request: TTSRequest):
    temp_file_path = None
    try:
        if not request.text:
            return JSONResponse(content={"error": "Text is required"}, status_code=400)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_file_path = temp_file.name
        
        tts = gTTS(text=request.text, lang='vi', slow=False)
        tts.save(temp_file_path)
        
        with open(temp_file_path, 'rb') as audio_file:
            audio_data = audio_file.read()
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        return {"audio": audio_base64}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except:
                pass
