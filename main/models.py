from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Test(models.Model):
    """Класс Теста"""
    title = models.CharField("Название теста", max_length=255)
    description = models.TextField("Описание теста", max_length=3000)
    completed = models.BooleanField('Заврешен ли тест', default=False)

    def __str__(self):
        return self.title[:30]

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = "Тесты"


class Question(models.Model):
    """Вопрос"""
    text = models.TextField('Текст вопроса', max_length=1000)
    test = models.ForeignKey(Test, verbose_name='тест', on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.text[:50]

    class Meta:
        verbose_name = 'Вопросы для теста'
        verbose_name_plural = 'Вопросы для теста'


class Options(models.Model):
    """Варианты ответов"""
    text = models.TextField('Текст ответа', max_length=1500)
    correct_answer = models.BooleanField(verbose_name='Правльный ответ', default=False)
    question = models.ForeignKey(Question, verbose_name='вопрос', on_delete=models.CASCADE, related_name='options')

    def __str__(self):
        return self.text[:50]

    class Meta:
        verbose_name = 'Вариант ответа для конкретного вопроса'
        verbose_name_plural = 'Варианты ответов для конкретного вопроса'


class Answer(models.Model):
    """Ответы пользователей"""
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.ForeignKey(Options, verbose_name='Выбранные вариант ответа', on_delete=models.CASCADE, null=True, blank=True)
    correct = models.BooleanField(verbose_name='Правильно ли ответил')
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = 'Ответ пользователя по каждому вопросу'
        verbose_name_plural = 'Ответы пользователя по каждому вопросу'


class Statistics(models.Model):
    """Стастика прохождеия тестов"""
    test = models.ForeignKey(Test, verbose_name='Тест', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, default=1)
    correct_ans = models.PositiveSmallIntegerField('Количество правильных ответов')

    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистика'
