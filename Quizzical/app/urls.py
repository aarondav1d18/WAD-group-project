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
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('account/', views.account, name='account'),
    path('create_quiz/', views.create_quiz, name='create_quiz'),
    path('category/', views.category, name='category'),
    path('quiz/<str:title>/', views.quiz, name='quiz'),
]