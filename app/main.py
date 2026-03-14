from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from presidio_analyzer import AnalyzerEngine

from app.indian_recognizers import (
    aadhaar_recognizer,
    pan_recognizer,
    phone_recognizer
)

from app.pii_vault import PIIVault


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