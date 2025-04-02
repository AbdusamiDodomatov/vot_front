from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class Election(models.Model):
    """Модель выборов"""
    name = models.CharField(max_length=255, unique=True, verbose_name="Название выборов")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    start_time = models.DateTimeField(verbose_name="Начало выборов")
    end_time = models.DateTimeField(verbose_name="Конец выборов")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        ordering = ["-start_time"]  # Последние выборы сверху
        verbose_name = "Выборы"
        verbose_name_plural = "Выборы"

    def __str__(self):
        return self.name


class Candidate(models.Model):
    """Модель кандидатов"""
    election = models.ForeignKey(
        Election, on_delete=models.CASCADE, related_name="candidates", verbose_name="Выборы"
    )
    name = models.CharField(max_length=255, verbose_name="Имя кандидата")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    class Meta:
        ordering = ["name"]  # Сортировка по имени кандидата
        verbose_name = "Кандидат"
        verbose_name_plural = "Кандидаты"

    def __str__(self):
        return f"{self.name} ({self.election.name})"


class ElectionVote(models.Model):
    """Модель голосов для выборов"""
    election = models.ForeignKey(
        Election, on_delete=models.CASCADE, related_name="votes", verbose_name="Выборы"
    )
    candidate = models.ForeignKey(
        Candidate, on_delete=models.CASCADE, related_name="votes", verbose_name="Кандидат"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="election_votes", verbose_name="Голосовавший"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата голосования")

    class Meta:
        unique_together = ("election", "user")  # Один пользователь – один голос
        verbose_name = "Голос (выборы)"
        verbose_name_plural = "Голоса (выборы)"

    def __str__(self):
        return f"{self.user.username} → {self.candidate.name}"


class Poll(models.Model):
    """Модель опросов"""
    question = models.CharField(max_length=255, verbose_name="Вопрос")
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="polls", verbose_name="Автор"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"

    def __str__(self):
        return self.question


class Choice(models.Model):
    """Модель вариантов ответа"""
    poll = models.ForeignKey(
        Poll, related_name="choices", on_delete=models.CASCADE, verbose_name="Опрос"
    )
    text = models.CharField(max_length=255, verbose_name="Вариант ответа")

    class Meta:
        ordering = ["text"]
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответов"

    def __str__(self):
        return self.text


class PollVote(models.Model):
    """Модель голосов для опросов"""
    poll = models.ForeignKey(
        Poll, on_delete=models.CASCADE, related_name="votes", verbose_name="Опрос"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="poll_votes", verbose_name="Голосовавший"
    )
    choice = models.ForeignKey(
        Choice, on_delete=models.CASCADE, related_name="votes", verbose_name="Выбранный вариант"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата голосования")

    class Meta:
        unique_together = ("poll", "user")  # Один пользователь – один голос в опросе
        verbose_name = "Голос (опрос)"
        verbose_name_plural = "Голоса (опросы)"

    def __str__(self):
        return f"{self.user.username} → {self.choice.text}"
