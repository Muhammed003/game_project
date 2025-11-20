from django.db import models

from apps.account.models import Country
from config import settings


# Create your models here.


class AudioTrack(models.Model):
    author = models.CharField(max_length=255, verbose_name="Автор", null=True, blank=True)
    title = models.CharField(max_length=255, verbose_name="Наименование трека")
    number_of_name = models.IntegerField(verbose_name="Номер имён")
    file = models.FileField(upload_to='audio/', verbose_name="Аудио файл")
    country = models.ForeignKey(
        "account.Country",  # или "Country", если модель в том же приложении
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Страна"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return f"{self.title} - {self.author}"


class WeeklyReport(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='users_weekly_report')
    fajr = models.PositiveIntegerField(default=0, verbose_name='Бомдод')
    isha = models.PositiveIntegerField(default=0, verbose_name='Хуфтон')
    tahajud = models.PositiveIntegerField(default=0, verbose_name='Тахажуд')
    lesson = models.PositiveIntegerField(default=0, verbose_name='Дарс')
    koran = models.PositiveIntegerField(default=0, verbose_name='Куръон')
    tafakkur = models.PositiveIntegerField(default=0, verbose_name='Тафаккур')
    create_date = models.DateField(auto_now_add=False, verbose_name="Дата добавления", null=True, blank=True)
    country = models.ForeignKey(
        to=Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Страна"
     )