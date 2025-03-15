from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    email = models.EmailField(unique=True) # Ensure only unique email addresses

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
        # Prevent deletion unless the user is a superuser
        request_user = kwargs.pop("request_user", None)
        if request_user is None or (
            not request_user.is_superuser
        ):
            raise PermissionDenied("You do not have permission to delete this category.")
        super().delete(*args, **kwargs)


class Quiz(models.Model):
    name = models.CharField(max_length=64)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
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

    def __str__(self):
        return self.name

    @staticmethod
    def get_default_category():
        """Returns a default category (e.g., 'Miscellaneous') if a quiz's category is deleted."""
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
    image = models.ImageField(upload_to="slides/images/", blank=True, null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="slides")


class Answer(models.Model):
    text = models.CharField(max_length=64)
    is_correct = models.BooleanField(default=False)
    slide = models.ForeignKey(Slide, on_delete=models.CASCADE, related_name="answers")