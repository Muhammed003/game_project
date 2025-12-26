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
    koran = models.PositiveIntegerField(default=0, verbose_name='Куръон')
    lesson = models.PositiveIntegerField(default=0, verbose_name='Такрор')
    tafakkur = models.PositiveIntegerField(default=0, verbose_name='Тафаккур')
    infok = models.PositiveIntegerField(default=0, verbose_name='Инфок')
    duo = models.PositiveIntegerField(default=0, verbose_name='Дуолар')
    zikr = models.PositiveIntegerField(default=0, verbose_name='Зикрлар')
    tahajud = models.PositiveIntegerField(default=0, verbose_name='Тахажжуд')
    ishrok = models.PositiveIntegerField(default=0, verbose_name='Ишрок')
    nafl_roza = models.PositiveIntegerField(default=0, verbose_name='Нафл роза')
    misvak = models.PositiveIntegerField(default=0, verbose_name='Мисвак')
    create_date = models.DateField(auto_now_add=False, verbose_name="Дата добавления", null=True, blank=True)
    country = models.ForeignKey(
        to=Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Страна"
     )

    @property
    def total_points(self):
        return (
                self.fajr + self.isha + self.tahajud + self.ishrok +
                self.koran + self.lesson + self.tafakkur + self.zikr +
                self.duo + self.infok + self.nafl_roza + self.misvak
        )