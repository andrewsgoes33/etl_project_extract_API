import requests
import json

url = 'https://api.openai.com/v1/chat/completions'

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer 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'
}

data = {
    'model': 'gpt-4o-mini',
    'messages': [{'role':'user', 'content':'Qual é a capital da França?'}]
}

response = requests.post(url, headers=headers, data=json.dumps(data))

print(response.json())