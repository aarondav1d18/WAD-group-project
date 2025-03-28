from django.contrib import admin
from .models import UserProfile, Category, Quiz, StarRating, Slide, Answer
from django.contrib import admin
from django.contrib.auth.models import User 

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'saved_quiz_list')
    search_fields = ('user__username', 'email')
    readonly_fields = ('saved_quiz_list',)

    def saved_quiz_list(self, obj):
        quizzes = obj.saved_quizes.all()
        return ", ".join(q.name for q in quizzes)

    saved_quiz_list.short_description = 'Saved Quizzes'



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
