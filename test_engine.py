from presidio_analyzer import AnalyzerEngine
from app.indian_recognizers import aadhaar_recognizer, pan_recognizer, phone_recognizer
from app.pii_vault import PIIVault

# Initialize analyzer engine
analyzer = AnalyzerEngine()

# Add custom recognization
analyzer.registry.add_recognizer(aadhaar_recognizer)
analyzer.registry.add_recognizer(pan_recognizer)
analyzer.registry.add_recognizer(phone_recognizer)

text = "My name is Rahul and my phone number is 9876543210."
# text = "Hello, I am Aman. My mobile number is +919876543210."
# text = "My name is Priya and my Aadhaar number is 1234-5678-9012."
# text = "User Ravi submitted Aadhaar 123456789012 for verification."
# text = "The PAN number of Rohit is ABCDE1234F."
# text = "My name is Neha, my PAN is QWERT1234Z, my Aadhaar is 1234 5678 9012 and phone is 919876543210."
# text = "Contact me at +919876543210 but my Aadhaar is 123456789012."
# text = "Rahul and Amit submitted their phone numbers 9876543210 and 9123456789."
# text = "Today the weather is very good and we are learning Python."
# text = "My name is Arjun, phone +919876543210, Aadhaar 1234-5678-9012 and PAN ASDFG1234H."

results = analyzer.analyze(
    text=text,
    entities=["PERSON","AADHAAR_NUMBER","PAN_NUMBER","INDIAN_PHONE_NUMBER"],
    language="en"
)
for result in results:
    print(result)

# create vault
vault = PIIVault()

masked = vault.mask_text(text,results)
print("Masked Text: ",masked)

ai_response = "I have noted that [PERSON_1] uses the number [INDIAN_PHONE_NUMBER_1]."
final = vault.unmask_text(ai_response)

print("Unmasked Text: ",final)