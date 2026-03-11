from presidio_analyzer import Pattern, PatternRecognizer

# Aadhaar Recognizer
aadhaar_pattern = Pattern(
    name="aadhaar_pattern",
    regex=r"\b(?!91[6-9])\d{4}[- ]?\d{4}[- ]?\d{4}\b",
    score=0.8
)

aadhaar_recognizer = PatternRecognizer(
    supported_entity="AADHAAR_NUMBER",
    patterns=[aadhaar_pattern]
)

# PAN Recognizer
pan_pattern = Pattern(
    name="pan_pattern",
    regex=r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b",
    score=0.8
)

pan_recognizer = PatternRecognizer(
    supported_entity="PAN_NUMBER",
    patterns=[pan_pattern]
)

# Indian Phone Recognizer
phone_pattern = Pattern(
    name="phone_pattern",
    regex=r"\b(\+?91[- ]?)?[6-9]\d{9}\b",
    score=0.8
)

phone_recognizer = PatternRecognizer(
    supported_entity="INDIAN_PHONE_NUMBER",
    patterns=[phone_pattern]
)