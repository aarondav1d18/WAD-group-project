import pytest
from django.test import TestCase
from app.models import Quiz, Question, Choice, UserProfile

class TestQuizModel(TestCase):
    def setUp(self):
        self.quiz = Quiz.objects.create(
            title="Test Quiz",
            description="Test Description"
        )

    def test_quiz_creation(self):
        self.assertEqual(self.quiz.title, "Test Quiz")
        self.assertEqual(self.quiz.description, "Test Description")

    def test_quiz_str(self):
        self.assertEqual(str(self.quiz), "Test Quiz")

class TestQuestionModel(TestCase):
    def setUp(self):
        self.quiz = Quiz.objects.create(title="Test Quiz")
        self.question = Question.objects.create(
            quiz=self.quiz,
            text="Test Question"
        )

    def test_question_creation(self):
        self.assertEqual(self.question.text, "Test Question")
        self.assertEqual(self.question.quiz, self.quiz)

class TestChoiceModel(TestCase):
    def setUp(self):
        self.quiz = Quiz.objects.create(title="Test Quiz")
        self.question = Question.objects.create(
            quiz=self.quiz,
            text="Test Question"
        )
        self.choice = Choice.objects.create(
            question=self.question,
            text="Test Choice",
            is_correct=True
        )

    def test_choice_creation(self):
        self.assertEqual(self.choice.text, "Test Choice")
        self.assertTrue(self.choice.is_correct)
        self.assertEqual(self.choice.question, self.question) 