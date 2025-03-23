from django.contrib import admin
from .models import UserProfile, Category, Quiz, StarRating, Slide, Answer

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'saved_quizes')
    search_fields = ('user__username', 'email')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_fun', 'created_by')
    search_fields = ('name',)
    list_filter = ('is_fun',)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'views', 'creation_date', 'category', 'created_by')
    search_fields = ('name',)
    list_filter = ('creation_date', 'category')


@admin.register(StarRating)
class StarRatingAdmin(admin.ModelAdmin):
    list_display = ('profile', 'quiz', 'stars')
    list_filter = ('stars',)


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1  # How many extra empty answer forms to display


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('question', 'quiz')
    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'is_correct', 'slide')
    search_fields = ('text',)
<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
