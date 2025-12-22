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
        fields = [
            "fajr", "isha", "tahajud", "lesson", "koran", "tafakkur",
            "infok", "duo", "zikr", "ishrok", "nafl_roza", "misvak"
        ]
        widgets = {
            "fajr": forms.NumberInput(attrs={"class": "form-control", "placeholder": "0"}),
            "isha": forms.NumberInput(attrs={"class": "form-control", "placeholder": "0"}),
            "tahajud": forms.NumberInput(attrs={"class": "form-control", "placeholder": "0"}),
            "lesson": forms.NumberInput(attrs={"class": "form-control", "placeholder": "0"}),
            "koran": forms.NumberInput(attrs={"class": "form-control", "placeholder": "0"}),
            "tafakkur": forms.NumberInput(attrs={"class": "form-control", "placeholder": "0"}),
            "infok": forms.NumberInput(attrs={"class": "form-control", "placeholder": "0"}),
            "duo": forms.NumberInput(attrs={"class": "form-control", "placeholder": "0"}),
            "zikr": forms.NumberInput(attrs={"class": "form-control", "placeholder": "0"}),
            "ishrok": forms.NumberInput(attrs={"class": "form-control", "placeholder": "0"}),
            "nafl_roza": forms.NumberInput(attrs={"class": "form-control", "placeholder": "0"}),
            "misvak": forms.NumberInput(attrs={"class": "form-control", "placeholder": "0"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Для новых объектов оставляем пустые поля
        if not self.instance.pk:
            for field in self.fields.values():
                field.initial = None
        # Все поля обязательны
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
