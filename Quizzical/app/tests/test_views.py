from django.test import TestCase, Client
from django.urls import reverse
from app.models import Quiz, Question, Choice, UserProfile
from django.contrib.auth.models import User

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.quiz = Quiz.objects.create(
            title="Test Quiz",
            description="Test Description"
        )

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/index.html')

    def test_quiz_detail_view(self):
        response = self.client.get(reverse('quiz_detail', args=[self.quiz.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/quiz_detail.html')

    def test_quiz_create_view_requires_login(self):
        response = self.client.get(reverse('quiz_create'))
        self.assertEqual(response.status_code, 302)  # Redirects to login

    def test_quiz_create_view_with_login(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('quiz_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/quiz_form.html') 