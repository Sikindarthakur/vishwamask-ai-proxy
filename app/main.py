from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from presidio_analyzer import AnalyzerEngine
from app.indian_recognizers import (
    aadhaar_recognizer,
    pan_recognizer,
    phone_recognizer
)
from app.pii_vault import PIIVault
import os
import time
from dotenv import load_dotenv
# from openai import OpenAI
from google import genai

load_dotenv()

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI(title="VishwaMask Privacy Proxy")


# --- Initialize analyzer ---
analyzer = AnalyzerEngine()

analyzer.registry.add_recognizer(aadhaar_recognizer)
analyzer.registry.add_recognizer(pan_recognizer)
analyzer.registry.add_recognizer(phone_recognizer)

vault = PIIVault()


# --- Request model ---
class PromptRequest(BaseModel):
    text: str


# --- API Endpoint ---
@app.post("/mask-prompt")
def mask_prompt(request: PromptRequest):

    text = request.text

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

    masked_text = vault.mask_text(text, results)

    return {
        "masked_text": masked_text,
        "entities_protected": len(results)
    }


@app.post("/chat")
def chat(request: PromptRequest):

    start_time = time.time()

    text = request.text

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

    # Step 2: mask
    masked_prompt = vault.mask_text(text, results)

    # Step 3: send to OpenAI
    # response = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[
    #         {"role": "user", "content": masked_prompt}
    #     ]
    # )

    # masked_reply = response.choices[0].message.content

    # Or send to Gemini

    try:
        # Note: 'models/' prefix is required for the v1beta API used by this SDK
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=masked_prompt  
        )
        masked_reply = response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API Error: {str(e)}")

    # Step 4: unmask
    final_reply = vault.unmask_text(masked_reply)

    latency = round(time.time() - start_time, 2)

    return {
        "original_prompt": text,
        "masked_prompt": masked_prompt,
        "ai_response": masked_reply,
        "unmask_response": final_reply,
        "latency_seconds": latency
    }