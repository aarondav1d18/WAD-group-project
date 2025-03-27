from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from app import models

# Create your views here.
def home(request):
    context = {
        'educational': [],
        'fun': []
    }
    try:
        quizzes = models.Quiz.objects.all()
        for quiz in quizzes:
            if quiz.category and quiz.category.is_fun:
                context['fun'].append(quiz)
            else:
                context['educational'].append(quiz)
    except Exception as e:
        print(f"Error loading quizzes: {e}")
    return render(request, 'app/base.html', context)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user and user.is_active:
            auth_login(request, user)
            return redirect(reverse('app:home'))
    return render(request, 'app/base.html')

def signup(request):
    return render(request, 'app/base.html')

@login_required
def account(request):
    return render(request, 'app/base.html')

@login_required
def create_quiz(request):
    return render(request, 'app/base.html')

def category(request):
    context = {'quizzes': []}
    try:
        quizzes = models.Quiz.objects.all()
        context['quizzes'] = quizzes
    except Exception as e:
        print(f"Error loading quizzes: {e}")
    return render(request, 'app/base.html', context)

def quiz(request):
    return render(request, 'app/base.html')