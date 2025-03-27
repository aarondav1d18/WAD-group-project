from django.shortcuts import render
import json
from app import models
# Create your views here.
import json
from django.shortcuts import render

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
                "image": quiz.image,  # Since `Quiz` has no `image` field dont know if we are going to add
                "rating": quiz_ratings[quiz.id]
            }
            if quiz.category and quiz.category.is_fun:
                context_dict["fun"].append(quiz_data)
            else:
                context_dict["educational"].append(quiz_data)

    except Exception as e:
        print(f"Error loading quizzes: {e}")  # Log error instead of silent failure

    return render(request, "app/home.html", {"quizzes": json.dumps(context_dict)})

def login(request):
    context = {'boldmessage': 'login'}
    return render(request, 'app/login.html', context)

def signup(request):
    context = {'boldmessage': 'signup'}
    return render(request, 'app/signup.html', context)

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