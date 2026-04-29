import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response

API_URL = f"Bearer{os.getenv('https://openrouter.ai/api/v1/chat/completions')}"
import os 
HEADERS = {
    "Authorization": "Bearer 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",
    "Content-Type": "application/json"
}

@api_view(['POST'])
def chatbot(request):
    messages = request.data.get('messages', [])

    try:
        response = requests.post(
    API_URL,
    headers=HEADERS,
    json={
        "model": "openai/gpt-3.5-turbo",
        "messages": messages,
        "max_tokens": 100
    },
    timeout=30
)
       

        data = response.json()
        print("FULL RESPONSE:", data)

        if "error" in data:
            return Response({"reply": data["error"]["message"]})

        reply = data["choices"][0]["message"]["content"]

        return Response({"reply": reply})

    except Exception as e:
        return Response({"reply": f"Error: {str(e)}"})