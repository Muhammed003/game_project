from django.db import models

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

