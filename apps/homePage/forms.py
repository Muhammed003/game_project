from django import forms

from apps.homePage.models import AudioTrack


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
