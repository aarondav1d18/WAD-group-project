from django.shortcuts import render
import json
import re
from app import models
# Create your views here.
import json

from app import models
from app.models import Quiz, Slide, Answer
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

import json
from app import models
from app.models import UserProfile, Quiz


# Create your views here.
def home(request):
    context_dict = {"educational": [], "fun": []}
    saved_ids = []
    if request.user.is_authenticated:
        user_profile, _ = models.UserProfile.objects.get_or_create(user=request.user)
        saved_ids = list(user_profile.saved_quizes.values_list('id', flat=True))

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
                "image": quiz.image,  # Since `Quiz` has no `image` field dont know if we are going to add
                "rating": quiz_ratings[quiz.id],
                "id": quiz.id,
                'saved_by_user': quiz.id in saved_ids
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

    # Include both the raw lists and the JSON version
    return render(request, "app/home.html", {
        "educational": context_dict["educational"],
        "fun": context_dict["fun"],
        "quizzes": json.dumps(context_dict)
    })


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
    errors = {}
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            user_profile = UserProfile.objects.get(email=email)
            # Use the related User's username for authentication
            user = authenticate(request, username=user_profile.user.username, password=password)
        except UserProfile.DoesNotExist:
            user = None
        
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse("app:home"))
            else:
                errors["email"] = "Your account is disabled."
        else:
            print(f"Invalid login details: {email}, {password}")
            errors["email"] = "Incorrect email or password."
    
    return render(request, "app/login.html", {"errors": errors})


def signup(request):
    errors = {}
    
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_confirmation = request.POST.get("password_confirmation")
        email_is_valid = True

        # Ensures that the email is in the name@example.com format
        try:
            validate_email(email)
        except ValidationError:
            email_is_valid = False
        
        # Username validation
        if len(username) < 3:
            errors["username"] = "Your username must be at least 3 characters long."
        elif len(username) > 32:
            errors["username"] = "Your username must be less than 32 characters long."
        elif not re.fullmatch(r"^[A-Za-z0-9_]+$", username):
            errors["username"] = "Your username can only contain letters, numbers, and underscores."
        elif User.objects.filter(username=username).exists():
            errors["username"] = "Your username must be unique."
        
        # Email validation
        if UserProfile.objects.filter(email=email).exists():
            errors["email"] = f"Your email is already registered with an account, try to <a href='{reverse('app:login')}'>log in</a> instead."
        elif not email_is_valid:
            errors["email"] = "Your email must be in the <i>name@example.com</i> format."
        
        # Password validation
        elif len(password) < 8:
            errors["password"] = "Your password must be at least 8 characters long."
        elif password != password_confirmation:
            errors["password"] = "Your password does not match with the confirmation."
        elif password.isupper() or password.islower():
            errors["password"] = f"Your password must contain at least one {'upper' if password.islower() else 'lower'}case letter."
        elif not re.search(r"\d", password):
            errors["password"] = "Your password must contain at least one number."
        
        if len(errors) == 0:
            # Create user profile in the database
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                UserProfile.objects.create(user=user, email=email)

                # Log in automatically after account creation
                return user_login(request)
            except Exception as e:
                errors["username"] = "There was a problem creating your account, please try again later."

    return render(request, 'app/signup.html', {"errors": errors})


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('app:home'))

@login_required
def account(request):
    context_dict = {"saved": [], "myQuizzes": [],}
    saved_ids = []
    user_profile, _ = models.UserProfile.objects.get_or_create(user=request.user)
    saved_ids = list(user_profile.saved_quizes.values_list('id', flat=True))

    try:
        savedQuizzes = [Quiz.objects.get(id=id) for id in saved_ids]
        myQuizzes = models.Quiz.objects.filter(created_by=user_profile)

        context_dict["userInfo"] = {
            'username': user_profile.user.username,
            'email': user_profile.user.email,
        }

        # Categorize quizzes
        for quiz in savedQuizzes:
            quiz_data = {
                "id": quiz.id,
                "title": quiz.name,
                "image": quiz.image,  # Since `Quiz` has no `image` field dont know if we are going to add
                'saved_by_user': quiz.id in saved_ids
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

            context_dict['saved'].append(quiz_data)

        for quiz in myQuizzes:
            quiz_data = {
                "id": quiz.id,
                "title": quiz.name,
                "image": quiz.image,  # Since `Quiz` has no `image` field dont know if we are going to add
                'saved_by_user': quiz.id in saved_ids
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

            context_dict['myQuizzes'].append(quiz_data)

    except Exception as e:
        print(f"Error loading quizzes: {e}")

    # Include both the raw lists and the JSON version
    return render(request, "app/account.html", {
        "quizzes": json.dumps(context_dict)
    })

@login_required
def create_quiz(request):
    return render(request, 'app/base.html')

def category(request):
    quiz_list = []
    saved_ids = []
    if request.user.is_authenticated:
        profile, _ = models.UserProfile.objects.get_or_create(user=request.user)
        saved_ids = list(profile.saved_quizes.values_list('id', flat=True))
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
                "rating": avg_rating,
                "user_rating": user_rating,
                "image": quiz.image,
                "category": category_name,
                "creation_date": quiz.creation_date.isoformat(),
                "id": quiz.id,
                'saved_by_user': quiz.id in saved_ids

            })
    except Exception as e:
        print("Error loading quizzes:", e)
    
    context = {"quizzes": json.dumps(quiz_list)}
    return render(request, "app/category.html", context)

def quiz(request, title):
    context = {}
    try:
        quiz = Quiz.objects.get(name=title)
        slides = Slide.objects.filter(quiz=quiz)

        context['name'] = quiz.name
        context['questions'] = {}
        context['answers'] = {}

        for i in range(0,slides.count()):
            context['questions'][i] = slides[i].question
            context['answers'][i] = [(answer.text, answer.is_correct) for answer in Answer.objects.filter(slide=slides[i])]
    except Exception as e:
        print("Error loading quiz:", e)

    return render(request, 'app/quiz.html', {'quiz': json.dumps(context)})
