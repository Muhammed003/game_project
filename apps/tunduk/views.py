from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
# Create your views here.

from django.shortcuts import render, redirect
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.http import HttpResponseForbidden

# Опционально: поставить rate-limit (см. подсказки ниже)
# from ratelimit.decorators import ratelimit

PIN_CODE = getattr(settings, "PIN_CODE", "2000")  # берём из settings / env

@require_http_methods(["GET", "POST"])
# @ratelimit(key='ip', rate='5/m', block=True)  # пример, если установлен django-ratelimit
def pin_view(request):
    if request.method == "POST":
        pin = request.POST.get("pin", "")
        # простая проверка — тайминг-атакам не уделяем внимание в простом примере
        if pin == PIN_CODE:
            # помечаем сессию как авторизованную
            request.session['pin_authenticated'] = True
            # можно записать время и т.п.: request.session['pin_time'] = timezone.now().isoformat()
            # делаем серверный редирект (без client JS)
            return redirect("/main/tun/main/")  # <-- путь по вашему проекту
        else:
            # неверный пин — добавим сообщение и вернём шаблон с сообщением
            messages.error(request, "ПИН туура эмес!")  # Kyrg or RU
            # или return HttpResponseForbidden("Неверный PIN")
            return render(request, "tunduk/tunduk_start_animation.html")  # имя шаблона (см. ниже)
    # GET
    return render(request, "tunduk/tunduk_start_animation.html")


class TunMainView(LoginRequiredMixin, TemplateView):
    template_name = 'tunduk/tunduk_main.html'

class DocumentsListView(LoginRequiredMixin, TemplateView):
    template_name = 'tunduk/documents_list.html'

class PassportView(LoginRequiredMixin, TemplateView):
    template_name = 'tunduk/passport.html'