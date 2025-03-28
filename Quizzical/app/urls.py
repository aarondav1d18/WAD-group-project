# path('login/', views.login),
#     path('signup/', views.signup),
#     path('account/', views.account),
#     path('create_quiz/', views.create_quiz),
#     path('category/', views.category),
#     path('quiz/', views.quiz),
from django.urls import path
from app import views

app_name = 'app'
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('account/', views.account, name='account'),
    path('create_quiz/', views.create_quiz, name='create_quiz'),
    path('category/', views.category, name='category'),
    path('quiz/', views.quiz, name='quiz'),
    path('logout/', views.user_logout, name='logout'),
    path('rate_quiz/', views.rate_quiz, name='rate_quiz'),
    path("save-quiz/", views.toggle_save_quiz, name="save_quiz"),
]