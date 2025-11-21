from django.shortcuts import render
from django.views.generic import TemplateView
from apps.account.mixins import RoleRequiredMixin
from apps.account.models import CustomUser, Country
from apps.homePage.models import AudioTrack, WeeklyReport


# Create your views here.
class ReportGroupView(RoleRequiredMixin, TemplateView):
    template_name = "report/reportgroup.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Все страны
        countries = Country.objects.all()

        groups_data = []

        for country in countries:
            users = CustomUser.objects.filter(country=country)

            # количество аудио в стране
            audio_count = AudioTrack.objects.filter(country=country).count()

            # недельные отчёты пользователей этой страны
            weekly_reports = WeeklyReport.objects.filter(country=country)

            # считаем сумму всех баллов по стране
            total_score = 0
            for item in weekly_reports:
                total_score += (
                    item.fajr
                    + item.isha
                    + item.tahajud
                    + item.lesson
                    + item.koran
                    + item.tafakkur
                )

            groups_data.append({
                "country": country,
                "users_count": users.count(),
                "audio_count": audio_count,
                "total_score": total_score,
                "last_week_reports": weekly_reports.order_by("-create_date")[:1],   # последние 1 неделя
                "all_reports": weekly_reports.order_by("-create_date")              # вся история
            })

        # сортируем по активности
        groups_sorted = sorted(groups_data, key=lambda x: x["total_score"], reverse=True)

        context["groups"] = groups_sorted
        return context
