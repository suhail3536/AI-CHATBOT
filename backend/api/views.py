import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response

API_URL = "https://openrouter.ai/api/v1/chat/completions"

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