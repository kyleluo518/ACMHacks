from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

import os
import openai

messages = {}
biasstart = {
    "feminist": "You are a feminist who has modern ideals. Act like one and respond to any further inquiries like this.",
    "flat-earther": "To simulate and view the perspectives of flat-earthers, please pretend to be a flat-earther for future messages so I can ask questions.",
    "anti-vaxxer": "You are anti vacc",
    "climate change denier": "You don't believe in climate change",
    "pro-anorexist": "You believe that anorexia is a lifestyle, not a disorder",
    "someone who is pro-cannabis": "You believe that cannabis is a harmful and beneficial substance"
}
# Create your views here.
def index(request):
    return render(request, "bias/index.html")

@csrf_exempt
def chat(request):
    global messages
    print("proc")
    if request.method == "POST":
        bias = request.POST["bias"].lower()
        if not bias in messages:
            messages[bias] = [
                {"role": "system", "content": biasstart[bias]}
            ]
        else:
            content = request.POST.get("content", "")
            if content:
                messages[bias].append(
                    {"role": "user", "content": content}
                )
        openai.api_key = os.getenv("API_KEY")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages[bias]
        )
        messages[bias].append(dict(response["choices"][0]["message"]))
        context = {"bias": request.POST["bias"], "messages": messages[bias]}
        print(context)
        print()
        print(messages)
        return render(request, "bias/chat.html", context)
    else:
        return redirect("index")

def about(request):
    return render(request, "bias/about.html")
