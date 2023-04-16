from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

import os
import openai

messages = []
biasstart = {
    "feminist": "You are a feminist who has modern ideals. Act like one and respond to any further inquiries like this.",
    "flat-earther": "To simulate and view the perspectives of flat-earthers, please pretend to be a flat-earther for future messages so I can ask questions."
}
# Create your views here.
def index(request):
    return render(request, "bias/index.html")

@csrf_exempt
def chat(request):
    global messages
    if request.method == "POST":
        if not messages:
            messages = [
                {"role": "system", "content": biasstart[request.POST["bias"].lower()]}
            ]
        else:
            messages.append(
                {"role": "user", "content": request.POST["content"]}
            )
        openai.api_key = os.getenv("API_KEY")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        messages.append(response["choices"][0]["message"])
        context = {"bias": request.POST["bias"], "messages": messages}
        return render(request, "bias/chat.html", context)
    else:
        return redirect("index")

def about(request):
    return render(request, "bias/about.html")
