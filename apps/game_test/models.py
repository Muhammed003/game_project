from django.db import models

from config import settings


class Level(models.Model):
    number = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Уровень {self.number}"

class Question(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()

    def __str__(self):
        return self.text

class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'правильный' if self.is_correct else 'неправильный'})"




# Create your models here.
class UserLevelResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    stars = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "level")  # ❗ первый результат сохраняется, остальные игнорируются

    def __str__(self):
        return f"{self.user} — {self.level} — {self.stars}⭐"
