from datetime import datetime, timedelta
from django.utils import timezone
from django.views.generic import TemplateView
from django.contrib import messages
from apps.account.mixins import RoleRequiredMixin
from apps.account.models import Country
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from datetime import timedelta


from apps.game_test.models import UserLevelResult
from apps.homePage.forms import AudioTrackForm, WeeklyReportForm
from apps.homePage.models import AudioTrack, WeeklyReport

CURRENCY_FLAGS = {
            "USD": "https://flagcdn.com/w320/us.png",
            "EUR": "https://flagcdn.com/w320/eu.png",
            "KGS": "https://flagcdn.com/w320/kg.png",
            "UZS": "https://flagcdn.com/w320/uz.png",
            "RUB": "https://flagcdn.com/w320/ru.png",
            "CNY": "https://flagcdn.com/w320/cn.png",
            "JPY": "https://flagcdn.com/w320/jp.png",
            "GBP": "https://flagcdn.com/w320/gb.png",
            "CHF": "https://flagcdn.com/w320/ch.png",
            "AUD": "https://flagcdn.com/w320/au.png",
            "CAD": "https://flagcdn.com/w320/ca.png",
            "BRL": "https://flagcdn.com/w320/br.png",
            "INR": "https://flagcdn.com/w320/in.png",
            "PKR": "https://flagcdn.com/w320/pk.png",
            "KZT": "https://flagcdn.com/w320/kz.png",
            "TJS": "https://flagcdn.com/w320/tj.png",
            "AFN": "https://flagcdn.com/w320/af.png",
            "IRR": "https://flagcdn.com/w320/ir.png",
            "SAR": "https://flagcdn.com/w320/sa.png",
            "AED": "https://flagcdn.com/w320/ae.png",
            "TRY": "https://flagcdn.com/w320/tr.png",
            "ILS": "https://flagcdn.com/w320/il.png",
            "KRW": "https://flagcdn.com/w320/kr.png",
            "SGD": "https://flagcdn.com/w320/sg.png",
            "MYR": "https://flagcdn.com/w320/my.png",
            "THB": "https://flagcdn.com/w320/th.png",
            "IDR": "https://flagcdn.com/w320/id.png",
            "PHP": "https://flagcdn.com/w320/ph.png",
            "VND": "https://flagcdn.com/w320/vn.png",
            "NZD": "https://flagcdn.com/w320/nz.png",
            "MXN": "https://flagcdn.com/w320/mx.png",
            "CLP": "https://flagcdn.com/w320/cl.png",
            "COP": "https://flagcdn.com/w320/co.png",
            "ARS": "https://flagcdn.com/w320/ar.png",
            "EGP": "https://flagcdn.com/w320/eg.png",
            "NGN": "https://flagcdn.com/w320/ng.png",
            "ZAR": "https://flagcdn.com/w320/za.png",
            "DKK": "https://flagcdn.com/w320/dk.png",
            "NOK": "https://flagcdn.com/w320/no.png",
            "SEK": "https://flagcdn.com/w320/se.png",
            "PLN": "https://flagcdn.com/w320/pl.png",
            "CZK": "https://flagcdn.com/w320/cz.png",
            "HUF": "https://flagcdn.com/w320/hu.png",
            "RON": "https://flagcdn.com/w320/ro.png",
            "BGN": "https://flagcdn.com/w320/bg.png",
            "HRK": "https://flagcdn.com/w320/hr.png",
            "UAH": "https://flagcdn.com/w320/ua.png",
            "BYN": "https://flagcdn.com/w320/by.png",
            "MDL": "https://flagcdn.com/w320/md.png",
            "GE": "https://flagcdn.com/w320/ge.png",
            "AM": "https://flagcdn.com/w320/am.png",
        }


class Main(TemplateView):
    template_name = "main/home.html"

class StartGameView(TemplateView):
    template_name = "main/start_game.html"


class SettingsGameView(TemplateView):
    template_name = "main/settings_game.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        countries = Country.objects.all()

        country_list = []
        for c in countries:
            country_list.append({
                "name": c.name,
                "flag": CURRENCY_FLAGS.get(c.name, ""),
                "code_password": c.code_password,
            })

        context["countries"] = country_list
        return context



@require_POST
@csrf_protect
def verify_country_code(request):
    """
    Ожидает POST с полями 'country' и 'code'.
    Возвращает JSON: {'ok': True, 'redirect': '/'} либо {'ok': False, 'error': '...'}
    """
    country_name = request.POST.get('country')
    code = request.POST.get('code', '').strip()

    if not country_name or not code:
        return JsonResponse({'ok': False, 'error': 'missing'}, status=400)

    try:
        country = get_object_or_404(Country, name=country_name)
    except Exception:
        return JsonResponse({'ok': False, 'error': 'no_country'}, status=404)

    # Если в модели хранится plain (нежелательно) — сравниваем. Лучше хранить хэш.
    if getattr(country, 'code_password', None) and country.code_password == code:
        # пометим в сессии, что доступ открыт
        request.session['country_verified'] = country.name
        # можно добавить время: request.session['country_verified_at'] = timezone.now().isoformat()
        # Вернуть безопасный относительный URL (избегать внешних редиректов)
        return JsonResponse({'ok': True, 'redirect': reverse('home')})
    else:
        return JsonResponse({'ok': False, 'error': 'wrong_code'}, status=403)


# GLAVNIY &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# class HomeBaseView(TemplateView):
#     template_name = "projects/home_main.html"

class HomeMainView(LoginRequiredMixin, TemplateView):
    template_name = "projects/home_main.html"

class NamesOfAllahView(LoginRequiredMixin, TemplateView):
    template_name = "projects/glavniy/alloh_ismlari.html"


class AudioListView(LoginRequiredMixin, TemplateView):
    template_name = "projects/glavniy/audio_of_names.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tracks'] = AudioTrack.objects.filter(
            country=self.request.user.country
        ).order_by('-created_at')
        return context


# PROFILE &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "projects/profile/profile.html"

    def get(self, request):
        results = UserLevelResult.objects.filter(user=request.user).order_by("level__number")

        total_stars = sum(r.stars for r in results)
        total_score = sum(r.score for r in results)
        max_level = max([r.level.number for r in results], default=0)

        return render(request, self.template_name, {
            "results": results,
            "total_stars": total_stars,
            "total_score": total_score,
            "max_level": max_level
        })





class AdministrationPageView(RoleRequiredMixin, TemplateView):
    template_name = "projects/profile/administration_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_country = None
        if self.request.user.country:
            code = self.request.user.country.name  # или name — что у тебя там
            user_country = CURRENCY_FLAGS.get(code)

        context["user_flag"] = user_country
        return context





class AudioAddPageView(RoleRequiredMixin, TemplateView):
    template_name = "projects/profile/audio_add.html"

    def get(self, request, action=None, pk=None):
        track = None
        if action == 'edit' and pk:
            track = get_object_or_404(AudioTrack, pk=pk, country=request.user.country)
            form = AudioTrackForm(instance=track)
        elif action == 'add':
            form = AudioTrackForm()
        elif action == 'delete' and pk:
            track = get_object_or_404(AudioTrack, pk=pk, country=request.user.country)
            track.delete()
            return redirect('administration-page_audio-add')
        else:
            form = AudioTrackForm()

        tracks = AudioTrack.objects.filter(country=request.user.country).order_by('-created_at')

        context = {
            'form': form,
            'tracks': tracks,
            'track': track
        }
        return render(request, self.template_name, context)

    def post(self, request, action=None, pk=None):
        track = None
        if action == 'edit' and pk:
            track = get_object_or_404(AudioTrack, pk=pk)
            form = AudioTrackForm(request.POST, request.FILES, instance=track)
        else:
            form = AudioTrackForm(request.POST, request.FILES)

        if form.is_valid():
            new_track = form.save(commit=False)
            new_track.country = request.user.country  # ✅ ставим страну пользователя
            new_track.save()
            return redirect('administration-page_audio-add')

        tracks = AudioTrack.objects.filter(country=request.user.country).order_by('-created_at')
        context = {
            'form': form,
            'tracks': tracks,
            'track': track
        }
        return render(request, self.template_name, context)
User = get_user_model()

class WeeklyReportAddView(LoginRequiredMixin, TemplateView):
    template_name = "projects/glavniy/weekly_report_add.html"

    def get(self, request, pk=None):
        report = None
        if pk:
            report = get_object_or_404(
                WeeklyReport,
                pk=pk,
                user=request.user
            )
            form = WeeklyReportForm(instance=report)
        else:
            form = WeeklyReportForm()

        # История пользователя
        history = WeeklyReport.objects.filter(user=request.user).order_by("-create_date")

        # Проверка на сегодняшний отчёт
        today_exists = WeeklyReport.objects.filter(
            user=request.user,
            create_date=now().date()
        ).exists()

        users_status = None
        if request.user.roles=="administrator" or request.user.roles=="chef":
            # Список всех пользователей и статус сдачи отчёта на этой неделе
            start_of_week = now().date() - timedelta(days=now().weekday())
            end_of_week = start_of_week + timedelta(days=6)

            users = User.objects.filter(country=self.request.user.country).order_by("username")
            users_status = []
            for u in users:
                report_exists = WeeklyReport.objects.filter(
                    user=u,
                    create_date__range=[start_of_week, end_of_week]
                ).exists()
                users_status.append({"user": u, "report_exists": report_exists})

        return render(request, self.template_name, {
            "form": form,
            "report": report,
            "history": history,
            "today_exists": today_exists,
            "users_status": users_status,
        })

    def post(self, request, pk=None):
        report = None
        if pk:
            report = get_object_or_404(WeeklyReport, pk=pk, user=request.user)
            form = WeeklyReportForm(request.POST, instance=report)
        else:
            if WeeklyReport.objects.filter(user=request.user, create_date=now().date()).exists():
                messages.error(request, "Вы уже добавили отчёт за сегодня.")
                return redirect("weekly-report-add")
            form = WeeklyReportForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.country = request.user.country
            if not pk and not obj.create_date:
                obj.create_date = now().date()
            obj.save()
            messages.success(request, "Отчёт сохранён!")
            return redirect("weekly-report-add")

        history = WeeklyReport.objects.filter(user=request.user).order_by("-create_date")
        return render(request, self.template_name, {
            "form": form,
            "history": history,
            "report": report
        })





class WeeklyReportListView(RoleRequiredMixin, TemplateView):
    template_name = "projects/glavniy/weekly_report_list.html"
    allowed_roles = ["admin", "administrator", "chef"]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        country = self.request.user.country
        show_all = self.request.GET.get("all") == "1"
        selected_date = self.request.GET.get("date")

        base_qs = WeeklyReport.objects.filter(
            user__country=country
        ).select_related("user")

        # 👉 список дат (ТОЛЬКО если история)
        available_dates = []
        if show_all:
            available_dates = (
                base_qs
                .values_list("create_date", flat=True)
                .distinct()
                .order_by("-create_date")
            )

        # 👉 фильтрация
        if show_all and selected_date:
            reports = base_qs.filter(create_date=selected_date)
        elif show_all:
            reports = base_qs.order_by("-create_date")
        else:
            start_week = timezone.now().date() - timedelta(days=7)
            reports = base_qs.filter(
                create_date__gte=start_week
            ).order_by("-create_date")

        ctx.update({
            "reports": reports,
            "show_all": show_all,
            "available_dates": available_dates,
            "selected_date": selected_date,
        })
        return ctx


class NamozTartibi(TemplateView):
    template_name = "projects/namoz_tartibi.html"
