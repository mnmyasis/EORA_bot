import re

from rest_framework import serializers

from app.models import DialogState, Question

POSITIVE_ANSWERS = ['конечно', 'ага', 'пожалуй', 'да']
NEGATIVE_ANSWERS = ['нет', 'ноуп', 'найн']


class MessageSerializer(serializers.Serializer):
    UNKNOWN_SLUG = 'unknown'

    message = serializers.CharField()
    user_id = serializers.CharField()

    def validate_message(self, value):
        if value is None:
            raise serializers.ValidationError('message is not null')
        return re.sub(r'/', '', value).lower()

    def search_answer(
            self,
            message,
            dialog_state: DialogState = None
    ) -> Question:
        question = None
        if dialog_state and dialog_state.current_question:
            if message in POSITIVE_ANSWERS:
                question = dialog_state.current_question.positive_answer
            elif message in NEGATIVE_ANSWERS:
                question = dialog_state.current_question.negative_answer
        if not question:
            questions = Question.objects.filter(slug=message)
            if questions.exists():
                question = questions.first()
            else:
                question = Question.objects.get(slug=self.UNKNOWN_SLUG)
        return question

    def dialog_state(self, user_id):
        dialog_states = DialogState.objects.filter(user=user_id)
        if dialog_states.exists():
            dialog_state = dialog_states.first()
            return dialog_state

    def save(self):
        user_id = self.validated_data['user_id']
        message = self.validated_data['message']
        dialog_state = self.dialog_state(user_id)
        question = self.search_answer(message, dialog_state)
        DialogState.objects.update_or_create(
            user=user_id,
            defaults={
                'user': user_id,
                'current_question': question
            }
        )
        return question
