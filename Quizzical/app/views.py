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

    try:
        quizzes = models.Quiz.objects.all()

        # Compute average ratings for display
        quiz_ratings = {}
        for quiz in quizzes:
            ratings = models.StarRating.objects.filter(quiz=quiz)
            avg_rating = sum(r.stars for r in ratings) / ratings.count() if ratings.exists() else 0
            quiz_ratings[quiz.id] = avg_rating

        # Order quizzes by rating
        quizzes = sorted(quizzes, key=lambda q: quiz_ratings[q.id], reverse=True)

        # Get current user's ratings if authenticated
        user_profile = request.user.profile if request.user.is_authenticated else None

        # Categorize quizzes
        for quiz in quizzes:
            quiz_data = {
                "id": quiz.id,
                "title": quiz.name,
                "image": quiz.image,  # adjust as needed
                "rating": quiz_ratings[quiz.id],
            }
            # Add user's rating if available
            if user_profile:
                try:
                    rating_obj = models.StarRating.objects.get(quiz=quiz, profile=user_profile)
                    quiz_data["user_rating"] = rating_obj.stars
                except models.StarRating.DoesNotExist:
                    quiz_data["user_rating"] = 0
            else:
                quiz_data["user_rating"] = 0

            if quiz.category and quiz.category.is_fun:
                context_dict["fun"].append(quiz_data)
            else:
                context_dict["educational"].append(quiz_data)

    except Exception as e:
        print(f"Error loading quizzes: {e}")

    return render(request, "app/home.html", {"quizzes": json.dumps(context_dict)})


@csrf_exempt
def rate_quiz(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"success": False, "error": "Not authenticated"}, status=403)
        try:
            data = json.loads(request.body)

            # Must match the JSON keys from the JS
            quiz_id = data.get("quiz_id")
            rating_value = data.get("rating")

            # Convert rating_value to an integer
            rating_value = int(rating_value)

            # (If rating_value is None or invalid, the above line will fail)
            quiz = models.Quiz.objects.get(id=quiz_id)
            print(rating_value)
            user_profile = request.user.profile
            rating_obj, created = models.StarRating.objects.get_or_create(
                quiz=quiz, profile=user_profile, defaults={"stars": rating_value}
            )
            # print(f'rating_obj: {rating_obj}    created: {created}')
            rating_obj.stars = rating_value
            rating_obj.save()

            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    else:
        return JsonResponse({"success": False, "error": "Invalid method"}, status=405)

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
    import json
    quiz_list = []
    try:
        quizzes = models.Quiz.objects.all()
        # If the user is authenticated, get their UserProfile for ratings
        user_profile = request.user.profile if request.user.is_authenticated else None

        for quiz in quizzes:
            # Calculate average rating using the reverse relation "ratings"
            ratings = quiz.ratings.all()
            if ratings.exists():
                avg_rating = sum(r.stars for r in ratings) / ratings.count()
            else:
                avg_rating = 0

            # Get the quiz's category name; if not set, default to "Miscellaneous"
            category_name = quiz.category.name if quiz.category else "Miscellaneous"
            
            # Get the logged-in user's rating for this quiz, if available
            if user_profile:
                try:
                    rating_obj = models.StarRating.objects.get(quiz=quiz, profile=user_profile)
                    user_rating = rating_obj.stars
                except models.StarRating.DoesNotExist:
                    user_rating = 0
            else:
                user_rating = 0
            
            # Build the quiz dictionary including the id and user_rating
            quiz_list.append({
                "id": quiz.id,  # Needed for rating submissions
                "title": quiz.name,
                "image": quiz.image,
                "rating": avg_rating,
                "user_rating": user_rating,
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