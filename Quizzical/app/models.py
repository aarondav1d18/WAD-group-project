import uuid
from email.policy import default

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied, ValidationError
from django.forms import UUIDField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    email = models.EmailField(unique=True)
    saved_quizes = models.ManyToManyField("Quiz", blank=True, related_name="saved_by_users")

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    is_fun = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="categories"
    )

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        request_user = kwargs.pop("request_user", None)
        if request_user is None or (not request_user.is_superuser):
            raise PermissionDenied("You do not have permission to delete this category.")
        super().delete(*args, **kwargs)


class Quiz(models.Model):
    name = models.CharField(max_length=64)
    id = models.AutoField(primary_key=True)
    views = models.IntegerField(default=0)
    creation_date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="quizzes",
    )
    created_by = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="quizzes"
    )
    # Image field to store the full path to the image (can be either static or media path)
    image = models.CharField(max_length=255, default='/static/images/default_quiz.jpg')

    def __str__(self):
        return self.name

    @staticmethod
    def get_default_category():
        default_category, _ = Category.objects.get_or_create(name="Miscellaneous")
        return default_category


class StarRating(models.Model):
    CHOICES = [(i, str(i)) for i in range(6)]
    stars = models.IntegerField(choices=CHOICES)
    profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="ratings"
    )
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="ratings")


class Slide(models.Model):
    question = models.CharField(max_length=256)
    image = models.ImageField(upload_to="media/", blank=True, null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="slides")


class Answer(models.Model):
    text = models.CharField(max_length=64)
    is_correct = models.BooleanField(default=False)
    slide = models.ForeignKey(Slide, on_delete=models.CASCADE, related_name="answers")

    def clean(self):
        if self.slide.answers.count() >= 4 and self.pk is None:
            raise ValidationError("A question can only have 4 answers")
        
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
