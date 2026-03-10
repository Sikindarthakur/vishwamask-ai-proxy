from presidio_analyzer import AnalyzerEngine

# Initialize analyzer engine
analyzer = AnalyzerEngine()

text = "My name is Rahul and my phone number is 9876543210"

results = analyzer.analyze(
    text=text,
    entities=["PERSON","PHONE_NUMBER"],
    language="en"
)
for result in results:
    print(result)