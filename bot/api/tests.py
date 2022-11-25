import json
from http import HTTPStatus

from django.test import TestCase, Client
from django.urls import reverse

from .serializers import POSITIVE_ANSWERS, NEGATIVE_ANSWERS


class MessageViewTest(TestCase):
    PATH_TO_FILE = './data/questions.json'
    fixtures = [PATH_TO_FILE]

    USER_ID = 'weqrrewr'
    URL_MESSAGE = reverse('api:message_view')
    RESPONSE_KEY = 'text'
    START_MESSAGE = '/start'
    CONTENT_TYPE = 'application/json'
    HEADERS = {
        'HTTP_USER_AGENT': 'django_unit_test_browser'
    }
    QUESTION_START = ''
    QUESTION_ABOUT_EARS = ''
    IS_CAT_ANSWER = ''
    IS_NOT_CAT_ANSWER = ''

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.load_bot_answer()

    @classmethod
    def load_bot_answer(cls):
        questions = []
        with open(cls.PATH_TO_FILE, encoding='utf-8') as file:
            data = json.load(file)
            for raw in data:
                questions.append(raw['fields']['text'])
        cls.QUESTION_START = questions[0]
        cls.QUESTION_ABOUT_EARS = questions[2]
        cls.IS_CAT_ANSWER = questions[1]
        cls.IS_NOT_CAT_ANSWER = questions[3]

    def request_post(self, user_id, message):
        data = {
            'user_id': user_id,
            'message': message
        }
        response = self.client.post(
            self.URL_MESSAGE,
            data=data,
            content_type=self.CONTENT_TYPE,
            **self.HEADERS
        )
        return response

    def check_answer(self, message, expected_answer):
        with self.subTest(message):
            response = self.request_post(self.USER_ID, self.START_MESSAGE)
            text = response.data.get(self.RESPONSE_KEY)
            self.assertEqual(text, self.QUESTION_START)
            response = self.request_post(self.USER_ID, message)
            text = response.data.get(self.RESPONSE_KEY)
            self.assertEqual(text, expected_answer)

    def test_response_key(self):
        response = self.request_post(self.USER_ID, self.START_MESSAGE)
        self.assertIsNotNone(response.data.get(self.RESPONSE_KEY))

    def test_status_code(self):
        response = self.request_post(self.USER_ID, self.START_MESSAGE)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_negative_and_positive_answer_message(self):
        for negative_answer, positive_answer in zip(NEGATIVE_ANSWERS,
                                                    POSITIVE_ANSWERS):
            self.check_answer(negative_answer, self.IS_CAT_ANSWER)
            self.check_answer(positive_answer, self.QUESTION_ABOUT_EARS)

    def test_is_cat(self):
        self.request_post(self.USER_ID, self.START_MESSAGE)
        response = self.request_post(self.USER_ID, 'да')
        self.assertEqual(response.data[self.RESPONSE_KEY],
                         self.QUESTION_ABOUT_EARS)
        response = self.request_post(self.USER_ID, 'да')
        self.assertEqual(response.data[self.RESPONSE_KEY], self.IS_CAT_ANSWER)

    def test_is_not_cat(self):
        self.request_post(self.USER_ID, self.START_MESSAGE)
        response = self.request_post(self.USER_ID, 'да')
        self.assertEqual(response.data[self.RESPONSE_KEY],
                         self.QUESTION_ABOUT_EARS)
        response = self.request_post(self.USER_ID, 'нет')
        self.assertEqual(response.data[self.RESPONSE_KEY],
                         self.IS_NOT_CAT_ANSWER)

    def test_not_valid_request(self):
        data = {
            'message': self.START_MESSAGE
        }
        response = self.client.post(self.URL_MESSAGE, data=data,
                                    content_type=self.CONTENT_TYPE,
                                    **self.HEADERS)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        data = {
            'user_id': self.USER_ID
        }
        response = self.client.post(self.URL_MESSAGE, data=data,
                                    content_type=self.CONTENT_TYPE,
                                    **self.HEADERS)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_register_message(self):
        response = self.request_post(self.USER_ID, '/StArT')
        self.assertEqual(response.data[self.RESPONSE_KEY], self.QUESTION_START)
