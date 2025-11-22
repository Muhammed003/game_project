from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.http import HttpResponseForbidden
from apps.game_test.models import Level, UserLevelResult, AnswerOption, Question
from django.views import View
from django.forms import modelform_factory, inlineformset_factory

from apps.homePage.forms import QuestionForm, AnswerFormSet, LevelForm


class LevelListView(LoginRequiredMixin, TemplateView):
    template_name = "test/levels.html"

    def get(self, request):
        levels = Level.objects.order_by("number")
        results = UserLevelResult.objects.filter(user=request.user)

        level_data = []
        completed_levels = {r.level_id: r for r in results}

        for lvl in levels:
            result = completed_levels.get(lvl.id)
            level_data.append({
                "level": lvl,
                "completed": bool(result),
                "stars": result.stars if result else 0,
                "locked": lvl.number != 1 and not completed_levels.get(lvl.number - 1),
            })

        return render(request, self.template_name, {"levels": level_data})

class LevelTestView(LoginRequiredMixin, TemplateView):
    template_name = "test/test.html"

    def get(self, request, level_number):
        level = get_object_or_404(Level, number=level_number)

        # запрет если уровень закрыт
        if level.number != 1:
            prev_completed = UserLevelResult.objects.filter(
                user=request.user, level__number=level.number - 1
            ).exists()
            if not prev_completed:
                return HttpResponseForbidden("Уровень ещё не открыт")

        questions = level.questions.prefetch_related("options")
        return render(request, self.template_name, {"level": level, "questions": questions})

    def post(self, request, level_number):
        level = get_object_or_404(Level, number=level_number)

        # если пользователь уже прошёл → нельзя перезаписать
        if UserLevelResult.objects.filter(user=request.user, level=level).exists():
            return redirect("levels")

        questions = level.questions.all()
        score = 0

        for q in questions:
            selected = request.POST.get(str(q.id))
            if selected and AnswerOption.objects.filter(id=selected, is_correct=True).exists():
                score += 1

        # считаем звёзды
        if score == 10:
            stars = 3
        elif score >= 7:
            stars = 2
        elif score >= 4:
            stars = 1
        else:
            stars = 0

        UserLevelResult.objects.create(
            user=request.user,
            level=level,
            score=score,
            stars=stars
        )

        return redirect("levels")

from django.contrib.auth import get_user_model

User = get_user_model()


class AdminTestStatsView(LoginRequiredMixin, TemplateView):
    template_name = "test/admin_stats.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.roles not in ["admin", "administrator", "chef"]:
            return HttpResponseForbidden("Нет доступа")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        users = User.objects.all().select_related("country").order_by("country")
        stats = []

        for user in users:
            results = UserLevelResult.objects.filter(user=user)
            if not results.exists():
                continue

            stats.append({
                "user": user,
                "country": user.country,
                "levels_completed": results.count(),
                "total_stars": sum(r.stars for r in results),
                "total_score": sum(r.score for r in results),
                "max_level": max([r.level.number for r in results]),
                "first_test": results.order_by("created_at").first().created_at,
            })

        # сортировка — лучшие наверху
        stats.sort(key=lambda x: (-x["total_stars"], -x["max_level"]))

        return render(request, self.template_name, {"stats": stats})



class QuestionAnswerCRUDView(View):
    template_name = 'test/question_answer_crud.html'

    def get(self, request, question_id=None):
        if question_id:
            question = get_object_or_404(Question, id=question_id)
        else:
            question = Question()
        q_form = QuestionForm(instance=question)
        a_formset = AnswerFormSet(instance=question)
        questions = Question.objects.all().prefetch_related('options')
        return render(request, self.template_name, {
            'q_form': q_form,
            'a_formset': a_formset,
            'questions': questions,
            'editing_question': question_id
        })

    def post(self, request, question_id=None):
        if question_id:
            question = get_object_or_404(Question, id=question_id)
        else:
            question = Question()
        q_form = QuestionForm(request.POST, instance=question)
        a_formset = AnswerFormSet(request.POST, instance=question)
        if q_form.is_valid() and a_formset.is_valid():
            q_form.save()
            a_formset.save()
            return redirect('question-answer-crud')
        questions = Question.objects.all().prefetch_related('options')
        return render(request, self.template_name, {
            'q_form': q_form,
            'a_formset': a_formset,
            'questions': questions,
            'editing_question': question_id
        })

def delete_answer(request, answer_id):
    answer = get_object_or_404(AnswerOption, id=answer_id)
    answer.delete()
    return redirect('question-answer-crud')


class LevelCRUDView(View):
    template_name = 'test/level_crud.html'

    def get(self, request, level_id=None):
        if level_id:
            level = get_object_or_404(Level, id=level_id)
        else:
            level = Level()
        form = LevelForm(instance=level)
        levels = Level.objects.all().order_by('number')
        return render(request, self.template_name, {
            'form': form,
            'levels': levels,
            'editing_level': level_id
        })

    def post(self, request, level_id=None):
        if level_id:
            level = get_object_or_404(Level, id=level_id)
        else:
            level = Level()
        form = LevelForm(request.POST, instance=level)
        if form.is_valid():
            form.save()
            return redirect('level-crud')
        levels = Level.objects.all().order_by('number')
        return render(request, self.template_name, {
            'form': form,
            'levels': levels,
            'editing_level': level_id
        })

def delete_level(request, level_id):
    level = get_object_or_404(Level, id=level_id)
    level.delete()
    return redirect('level-crud')