from django.test import TestCase

from app.models import Question


class QuestionTest(TestCase):
    fixtures = ['./data/questions.json']

    START_SLUG = 'start'
    UNKNOWN_SLUG = 'unknown'
    EXPECTED_QUESTION_MINIMAL_COUNT = 2

    def test_question_slug(self):
        question = Question.objects.filter(slug=self.START_SLUG).exists()
        self.assertTrue(question)
        question = Question.objects.filter(slug=self.UNKNOWN_SLUG).exists()
        self.assertTrue(question)

    def test_minimal_question_count(self):
        count = Question.objects.count()
        self.assertGreater(count, self.EXPECTED_QUESTION_MINIMAL_COUNT)

