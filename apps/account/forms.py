from django import forms
from .models import CustomUser


class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
        required=True
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number', 'roles', 'is_active', 'country']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+996...'}),
            'roles': forms.Select(attrs={'class': 'form-select'}),
            'country': forms.Select(attrs={'class': 'form-select'}),
        }

    # получаем request
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

        # ----- Если НЕ admin -----
        if self.request.user.roles != "admin":
            # скрываем поля
            self.fields['roles'].widget = forms.HiddenInput()
            self.fields['country'].widget = forms.HiddenInput()
            self.fields['is_active'].widget = forms.HiddenInput()

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        user.set_password(password)

        # ----- Если НЕ admin -----
        if self.request.user.roles != "admin":
            user.roles = "employee"
            user.country = self.request.user.country
            user.is_active = True  # или оставить как есть

        if commit:
            user.save()

        return user
