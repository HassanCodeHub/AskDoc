import requests
import json


url = "http://127.0.0.1:5000/api/questions/ask/stream"

payload = {
    "document_id": 47,
    "question": "What are the steps for implementing a stack using linked list?"
}


response = requests.post(
    url,
    json=payload,
    stream=True
)


print("STATUS:", response.status_code)
print("CONTENT TYPE:", response.headers.get("Content-Type"))
print("\nSTREAM:\n")


for line in response.iter_lines(decode_unicode=True):

    if not line:
        continue

    data = json.loads(line)

    print(data)