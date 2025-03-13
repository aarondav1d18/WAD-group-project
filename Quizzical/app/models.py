#! the hashbang marks points of interest in this file. delete this if there are none remaining.
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    email = models.CharField(max_length=320)

    user = models.OneToOneField(User, on_delete = models.CASCADE) #mapping a UserProfile to a user model instance

    def __str__(self):
        return self.user.username
    

class Category(models.Model):

    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Quiz(models.Model):

    name = models.CharField(max_length=64)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    creation_date = models.DateField(auto_now_add=True)

    category = models.ForeignKey(Category, on_delete=models.PROTECT) #!categories with 1 or more quizzes now cannot be deleted - do we want this? if not, change PROTECT to SET_NULL.
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name #!what if two quizzes have the same name. add creation date?
    

class StarRating(models.Model):

    CHOICES = [(i, str(i)) for i in range(6)]
    stars = models.IntegerField(choices = CHOICES)

    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)


class Slide(models.Model):

    question = models.CharField(max_length=256)
    image_url = models.URLField() #! changed from Char(128) on the design spec - should we use ImageField instead?

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)


class Answer(models.Model):

    text = models.CharField(max_length=64)
    is_correct = models.BooleanField(default=False)

    slide = models.ForeignKey(Slide, on_delete=models.CASCADE)

