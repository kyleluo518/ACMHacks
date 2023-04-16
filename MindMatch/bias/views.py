from django.shortcuts import render

# Create your views here.
def index(request):
    render("index.html")

def chat(request):
    render("chat.html")

def about(request):
    render("about.html")
