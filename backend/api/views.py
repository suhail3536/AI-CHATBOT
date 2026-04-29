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
    "model": "openai/gpt-3.5-turbo",
    "messages": messages,
    "max_tokens": 100
}
            timeout=40
        )

        data = response.json()
        print("FULL RESPONSE:", data)

        if "error" in data:
            return Response({"reply": data["error"]["message"]})

        reply = data["choices"][0]["message"]["content"]

        return Response({"reply": reply})

    except Exception as e:
        return Response({"reply": f"Error: {str(e)}"})