from django import forms

from apps.game_test.models import Question, AnswerOption, Level
from apps.homePage.models import AudioTrack, WeeklyReport


class AudioTrackForm(forms.ModelForm):
    class Meta:
        model = AudioTrack
        fields = ['title', 'number_of_name', 'file']  # author не показываем!

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)   # получаем request.user
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        obj = super().save(commit=False)
        if self.user:
            obj.author = self.user   # автор автоматически
        if commit:
            obj.save()
        return obj


class WeeklyReportForm(forms.ModelForm):
    class Meta:
        model = WeeklyReport
        fields = ["fajr", "isha", "tahajud", "lesson", "koran", "tafakkur"]
        widgets = {
            "fajr": forms.NumberInput(attrs={"class": "form-control", "value": "", "placeholder":"0"}),
            "isha": forms.NumberInput(attrs={"class": "form-control", "value": "", "placeholder":"0"}),
            "tahajud": forms.NumberInput(attrs={"class": "form-control", "value": "", "placeholder":"0"}),
            "lesson": forms.NumberInput(attrs={"class": "form-control", "value": "", "placeholder":"0"}),
            "koran": forms.NumberInput(attrs={"class": "form-control", "value": "", "placeholder":"0"}),
            "tafakkur": forms.NumberInput(attrs={"class": "form-control", "value": "", "placeholder":"0"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ❗ Передаём пустой value вместо 0
        for name, field in self.fields.items():
            if not self.instance.pk:  # Только при создании
                field.initial = None

        # ❗ Делаем поля обязательными
        for field in self.fields.values():
            field.required = True



class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['level', 'text']
        widgets = {
            'level': forms.Select(attrs={'class':'form-select'}),
            'text': forms.Textarea(attrs={'class':'form-control', 'rows':3}),
        }

from django.forms import inlineformset_factory
AnswerFormSet = inlineformset_factory(
    Question, AnswerOption,
    fields=['text', 'is_correct'],
    extra=4,
    can_delete=True,
    widgets={
        'text': forms.TextInput(attrs={'class':'form-control'}),
        'is_correct': forms.CheckboxInput(attrs={'class':'form-check-input'}),
    }
)


class LevelForm(forms.ModelForm):
    class Meta:
        model = Level
        fields = ['number', 'name']
        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
