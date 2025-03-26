from django.test import TestCase
from django.db import IntegrityError
from app.models import Quiz, Question, Choice, UserProfile
from django.contrib.auth.models import User

class TestDatabaseIntegrity(TestCase):
    def test_quiz_cascade_delete(self):
        quiz = Quiz.objects.create(title="Test Quiz")
        question = Question.objects.create(quiz=quiz, text="Test Question")
        choice = Choice.objects.create(question=question, text="Test Choice")
        
        # Delete quiz should cascade to questions and choices
        quiz.delete()
        self.assertEqual(Question.objects.count(), 0)
        self.assertEqual(Choice.objects.count(), 0)

    def test_question_cascade_delete(self):
        quiz = Quiz.objects.create(title="Test Quiz")
        question = Question.objects.create(quiz=quiz, text="Test Question")
        choice = Choice.objects.create(question=question, text="Test Choice")
        
        # Delete question should cascade to choices
        question.delete()
        self.assertEqual(Choice.objects.count(), 0)

    def test_unique_constraints(self):
        # Test that we can't create duplicate quiz titles
        Quiz.objects.create(title="Unique Quiz")
        with self.assertRaises(IntegrityError):
            Quiz.objects.create(title="Unique Quiz")

    def test_choice_correct_answer_constraint(self):
        quiz = Quiz.objects.create(title="Test Quiz")
        question = Question.objects.create(quiz=quiz, text="Test Question")
        
        # Test that we can't have multiple correct answers
        Choice.objects.create(question=question, text="Choice 1", is_correct=True)
        with self.assertRaises(IntegrityError):
            Choice.objects.create(question=question, text="Choice 2", is_correct=True) 