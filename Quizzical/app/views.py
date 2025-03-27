from django.shortcuts import render
import json
from app import models
# Create your views here.
import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app import models
# Create your views here.
def home(request):
    context_dict = {"educational": [], "fun": []}
    saved_ids = []
    if request.user.is_authenticated:
        user_profile, _ = models.UserProfile.objects.get_or_create(user=request.user)
        saved_ids = list(user_profile.saved_quizes.values_list('id', flat=True))

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
                "rating": quiz_ratings[quiz.id],
                "id": quiz.id,
                'saved_by_user': quiz.id in saved_ids
            }
            if quiz.category and quiz.category.is_fun:
                context_dict["fun"].append(quiz_data)
            else:
                context_dict["educational"].append(quiz_data)

    except Exception as e:
        print(f"Error loading quizzes: {e}")  # Log error instead of silent failure

    return render(request, "app/home.html", {"quizzes": json.dumps(context_dict)})


@csrf_exempt
@login_required
def toggle_save_quiz(request):
    if request.method == "POST":
        data = json.loads(request.body)
        quiz_id = data.get("quiz_id")
        try:
            quiz = models.Quiz.objects.get(id=quiz_id)
            profile, _ = models.UserProfile.objects.get_or_create(user=request.user, defaults={'email': request.user.email})

            if quiz in profile.saved_quizes.all():
                profile.saved_quizes.remove(quiz)
                return JsonResponse({"success": True, "action": "unsaved"})
            else:
                profile.saved_quizes.add(quiz)
                return JsonResponse({"success": True, "action": "saved"})

        except models.Quiz.DoesNotExist:
            return JsonResponse({"success": False, "message": "Quiz not found"}, status=404)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)



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
    context = {'boldmessage': 'signup'}
    return render(request, 'app/base.html', context)

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('app:home'))

def account(request):
    ## Gonna leave the account urls up to whoever does it
    context = {'boldmessage': 'account'}
    return render(request, 'app/base.html', context)

def create_quiz(request):
    context = {'boldmessage': 'create_quiz'}
    return render(request, 'app/base.html', context)

def category(request):
    quiz_list = []
    saved_ids = []
    if request.user.is_authenticated:
        profile, _ = models.UserProfile.objects.get_or_create(user=request.user)
        saved_ids = list(profile.saved_quizes.values_list('id', flat=True))
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
                "creation_date": quiz.creation_date.isoformat(),
                "id": quiz.id,
                'saved_by_user': quiz.id in saved_ids

            })
    except Exception as e:
        print("Error loading quizzes:", e)
    
    context = {"quizzes": json.dumps(quiz_list)}
    return render(request, "app/category.html", context)


def quiz(request):
    context = {'boldmessage': 'quiz'}
    return render(request, 'app/base.html', context)