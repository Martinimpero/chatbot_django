import json
import asyncio
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Initialize chatbot
template = """
Answer the question below

Here is the conversation history: {context}

Question: {question}

Answer:
"""
model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


def chatbot_view(request):
    chat_history = request.session.get("chat_history", "").splitlines()
    return render(request, "chatbot/chat.html", {"chat_history": chat_history})


@csrf_exempt
def chatbot_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "").strip()

        if not user_message:
            return JsonResponse({"error": "Empty message"}, status=400)

        chat_history = request.session.get("chat_history", "")

        # Get AI response
        response = asyncio.run(asyncio.to_thread(chain.invoke, {"context": chat_history, "question": user_message}))

        # Update session history
        chat_history += f"\nUser: {user_message}\nBot: {response}"
        request.session["chat_history"] = chat_history

        return JsonResponse({"response": response})
