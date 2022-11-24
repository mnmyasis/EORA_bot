from django.db import models


class DialogState(models.Model):
    user = models.CharField(max_length=256)
    current_question = models.ForeignKey(
        'Question',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='dialog_states'
    )


class Question(models.Model):
    text = models.TextField()
    positive_answer = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Следующий вопрос в случае положительного ответа',
        related_name='positive_answers'
    )
    negative_answer = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Следующий вопрос в случае негативного ответа',
        related_name='negative_answers'
    )
    slug = models.SlugField(unique=True, blank=True, null=True)

    class Meta:
        default_related_name = 'questions'

    def __str__(self):
        return self.text
