from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class Message(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "CUTIE Backend Running!"}

@app.post("/api/ask")
def ask_ai(data: Message):
    user_msg = data.message

    chat = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "system", "content": "You are CUTIE, a friendly helper AI for students."},
        {"role": "user", "content": user_msg}
    ]
)


    reply = chat.choices[0].message.content
    return {"reply": reply}
