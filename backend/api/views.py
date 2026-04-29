import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response

API_URL = "https://openrouter.ai/api/v1/chat/completions"
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
                "model": "meta-llama/llama-3-8b-instruct",
                "messages": messages,
                "max_tokens": 100
            },
            timeout=15
        )

        data = response.json()
        print("FULL RESPONSE:", data)

        if "error" in data:
            return Response({"reply": data["error"]["message"]})

        reply = data["choices"][0]["message"]["content"]

        return Response({"reply": reply})

    except Exception as e:
        return Response({"reply": f"Error: {str(e)}"})