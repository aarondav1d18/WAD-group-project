from django.shortcuts import render

# Create your views here.
def home(request):
    ## Using empty context for now and base.html just to set up
    ## the views and urls
    context = {'boldmessage': 'home'}
    return render(request, 'app/base.html', context)

def login(request):
    context = {'boldmessage': 'login'}
    return render(request, 'app/base.html', context)

def signup(request):
    context = {'boldmessage': 'signup'}
    return render(request, 'app/base.html', context)

def account(request):
    ## Gonna leave the account urls up to whoever does it
    context = {'boldmessage': 'account'}
    return render(request, 'app/base.html', context)

def create_quiz(request):
    context = {'boldmessage': 'create_quiz'}
    return render(request, 'app/base.html', context)

def category(request):
    context = {'boldmessage': 'category'}
    return render(request, 'app/base.html', context)

def quiz(request):
    context = {'boldmessage': 'quiz'}
    return render(request, 'app/base.html', context)