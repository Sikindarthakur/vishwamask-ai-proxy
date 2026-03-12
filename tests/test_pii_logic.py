import pytest
from presidio_analyzer import AnalyzerEngine
from app.indian_recognizers import aadhaar_recognizer, pan_recognizer, phone_recognizer
from app.pii_vault import PIIVault


def setup_engine():

    analyzer = AnalyzerEngine()

    analyzer.registry.add_recognizer(aadhaar_recognizer)
    analyzer.registry.add_recognizer(pan_recognizer)
    analyzer.registry.add_recognizer(phone_recognizer)

    return analyzer


# Test 1: name + phone
def test_phone_masking():

    analyzer = setup_engine()
    vault = PIIVault()

    text = "My name is Rahul and my phone is +919876543210"

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

    masked = vault.mask_text(text, results)

    assert "[PERSON_1]" in masked or "[NAME_1]" in masked
    assert "[INDIAN_PHONE_NUMBER_1]" in masked


# Test 2: Aadhaar detection
def test_aadhaar_masking():

    analyzer = setup_engine()
    vault = PIIVault()

    text = "My Aadhaar is 1234-5678-9012"

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

    masked = vault.mask_text(text, results)

    assert "[AADHAAR_NUMBER_1]" in masked


# Test 3: deterministic masking
def test_same_name_token():

    analyzer = setup_engine()
    vault = PIIVault()

    text = "Rahul met Rahul yesterday"

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

    masked = vault.mask_text(text, results)

    assert masked.count("[PERSON_1]") == 2


# Test 4: no pii
def test_no_pii():

    analyzer = setup_engine()
    vault = PIIVault()

    text = "Today the weather is nice"

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

    masked = vault.mask_text(text, results)

    assert masked == text


# Test 5: PAN detection
def test_pan_masking():

    analyzer = setup_engine()
    vault = PIIVault()

    text = "My PAN is ABCDE1234F"

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
    masked = vault.mask_text(text, results)

    assert "[PAN_NUMBER_1]" in masked