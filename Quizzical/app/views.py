from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse
import json
from app import models

# Create your views here.
def home(request):
    context_dict = {"educational": [], "fun": []}

    try:
        # Fetch quizzes
        quizzes = models.Quiz.objects.all()

        # Compute average ratings
        quiz_ratings = {}
        for quiz in quizzes:
            ratings = models.StarRating.objects.filter(quiz=quiz)
            avg_rating = sum(r.stars for r in ratings) / ratings.count() if ratings.exists() else 0
            quiz_ratings[quiz.id] = avg_rating

        # Order quizzes by rating
        quizzes = sorted(quizzes, key=lambda q: quiz_ratings[q.id], reverse=True)

        # Categorize quizzes
        for quiz in quizzes:
            quiz_data = {
                "title": quiz.name,
                "rating": quiz_ratings[quiz.id]
            }
            if quiz.category and quiz.category.is_fun:
                context_dict["fun"].append(quiz_data)
            else:
                context_dict["educational"].append(quiz_data)

    except Exception as e:
        print(f"Error loading quizzes: {e}")

    return render(request, "app/home.html", {"quizzes": json.dumps(context_dict)})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('app:home'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'app/login.html')

def signup(request):
    return render(request, 'app/base.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('app:home'))

@login_required
def account(request):
    return render(request, 'app/base.html')

@login_required
def create_quiz(request):
    return render(request, 'app/base.html')

def category(request):
    quiz_list = []
    try:
        quizzes = models.Quiz.objects.all()
        for quiz in quizzes:
            # Use the reverse relation to get ratings for this quiz
            ratings = quiz.ratings.all()
            if ratings.exists():
                avg_rating = sum(r.stars for r in ratings) / ratings.count()
            else:
                avg_rating = 0

            # If no category is associated, display "Miscellaneous"
            category_name = quiz.category.name if quiz.category else "Miscellaneous"
            
            quiz_list.append({
                "title": quiz.name,
                "rating": avg_rating,
                "category": category_name,
                "creation_date": quiz.creation_date.isoformat()
            })
    except Exception as e:
        print("Error loading quizzes:", e)
    
    context = {"quizzes": json.dumps(quiz_list)}
    return render(request, "app/category.html", context)

def quiz(request):
    return render(request, 'app/base.html')