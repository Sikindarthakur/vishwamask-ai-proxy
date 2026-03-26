import os
import time
import httpx
import html
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException , BackgroundTasks
from pydantic import BaseModel, Field
from typing import Literal
from presidio_analyzer import AnalyzerEngine
from app.indian_recognizers import (
    aadhaar_recognizer,
    pan_recognizer,
    phone_recognizer,
    name_pattern
)
from app.pii_vault import PIIVault

from openai import OpenAI
from google import genai

from app.database import engine
from app.models import Base
from app.database import SessionLocal
from app.models import Log


Base.metadata.create_all(bind=engine)

load_dotenv()

OLLAMA_BASE = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_DEFAULT_MODEL", "llama3")

# Initialize OpenAI Client
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize Gemini Client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

app = FastAPI(title="VishwaMask Privacy Proxy")


# --- Initialize analyzer ---
analyzer = AnalyzerEngine()
analyzer.registry.add_recognizer(aadhaar_recognizer)
analyzer.registry.add_recognizer(pan_recognizer)
analyzer.registry.add_recognizer(phone_recognizer)
analyzer.registry.add_recognizer(name_pattern)

# --- Request model ---
class PromptRequest(BaseModel):
    text: str = Field(..., max_length=5000)
    provider: Literal["ollama", "openai", "gemini"] = "ollama"
    model: str | None = None

def save_logs(provider, results, latency):
    from app.database import SessionLocal
    from app.models import Log

    db = SessionLocal()

    if results:
        for entity in results:
            log = Log(
                provider=provider,
                entity_type=entity.entity_type,
                latency=latency
            )
            db.add(log)
    else:
        log = Log(
            provider=provider,
            entity_type="NO_PII",
            latency=latency
        )
        db.add(log)

    db.commit()
    db.close()

# --- API Endpoint ---
@app.post("/mask-prompt")
async def mask_prompt(request: PromptRequest):

    text = html.escape(request.text)

    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    results = analyzer.analyze(
        text=text,
        language="en",
        entities=[
            "PERSON",
            "AADHAAR_NUMBER",
            "PAN_NUMBER",
            "INDIAN_PHONE_NUMBER"
        ]
    )
    vault = PIIVault()
    masked_text = vault.mask_text(text, results)

    return {
        "original_text": text,
        "masked_text": masked_text,
        "entities_protected": len(results)
    }


@app.post("/chat")
async def chat(request: PromptRequest, background_tasks: BackgroundTasks):
    text = request.text.strip()
    provider = request.provider
    model = request.model or OLLAMA_MODEL

    # ✅ sanitize input
    text = html.escape(text)

    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    # Step 1: detect PII
    results = analyzer.analyze(
        text=text,
        language="en",
        entities=[
            "PERSON",
            "AADHAAR_NUMBER",
            "PAN_NUMBER",
            "INDIAN_PHONE_NUMBER"
        ]
    )

    # Step 2: Create a per-request vault and mask
    vault = PIIVault()
    masked_prompt = vault.mask_text(text, results)

    start_time = time.time()


    # Step 3: Provider branching
    if provider == "ollama":
        # Ollama REST chat endpoint: /api/chat (or /api/generate)
        url = f"{OLLAMA_BASE.rstrip('/')}/api/chat"
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": masked_prompt}],
            "stream": False
        }
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, json=payload, timeout=60)
                resp.raise_for_status()
                data = resp.json()

            masked_reply = data.get("message", {}).get("content", "")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ollama error: {e}")
        
    elif provider == "openai":

        if not OPENAI_API_KEY:
            raise HTTPException(
                status_code=400,
                detail="OpenAI API key not configured."
            )
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": masked_prompt
                    }
                ]
            )

            masked_reply = response.choices[0].message.content

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"OpenAI error: {str(e)}"
            )
        
    elif provider == "gemini":

        if not GEMINI_API_KEY:
            raise HTTPException(
                status_code=400,
                detail="Gemini API key not configured."
            )

        try:
            response = gemini_client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=masked_prompt
            )

            masked_reply = response.text

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Gemini error: {str(e)}"
            )

    # Step 4: unmask
    final_reply = vault.unmask_text(masked_reply)
    # leak detection
    latency = round(time.time() - start_time, 3)
    # leak detection
    leaks = vault.detect_leak(masked_reply)
    background_tasks.add_task(save_logs, provider, results, latency)
    return {
        "original_prompt": text,
        "masked_prompt": masked_prompt,
        "ai_response": masked_reply,
        "unmask_response": final_reply,
        "entities_protected": len(vault.vault_registry) if hasattr(vault, "vault_registry") else len(vault.unmask_map),
        "leak_count": len(leaks),
        "latency_seconds": latency
    }