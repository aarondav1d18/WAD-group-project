from django.shortcuts import render
from app import models
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
    import json
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
                "image": quiz.image,
                "rating": avg_rating,
                "category": category_name,
                "creation_date": quiz.creation_date.isoformat()
            })
    except Exception as e:
        print("Error loading quizzes:", e)
    
    context = {"quizzes": json.dumps(quiz_list)}
    return render(request, "app/category.html", context)


def quiz(request):
    context = {'boldmessage': 'quiz'}
    return render(request, 'app/base.html', context)