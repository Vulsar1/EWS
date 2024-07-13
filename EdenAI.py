import json
import requests

headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZTlhNTIwZmYtZmY4Mi00M2ViLTk0NzItNGZjNjU4YTFjZTJkIiwidHlwZSI6ImFwaV90b2tlbiJ9.QR7fQciG_xlWQRe2wEz9on1rmC4o3ukdoEkCZ27xB6M"}

url = "https://api.edenai.run/v2/text/chat"
payload = {
    "providers": "openai",
    "text": "Hello i need your help ! ",
    "chatbot_global_action": "Act as an assistant",
    "previous_history": [],
    "temperature": 0.0,
    "max_tokens": 150,
}

response = requests.post(url, json=payload, headers=headers)

result = json.loads(response.text)
print(result['openai']['generated_text'])
