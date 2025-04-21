from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User  # Только этот импорт нужен!
import re  # ← импорт переместили сюда

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Логин")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

class CustomUserCreationForm(UserCreationForm):
    passport_series = forms.CharField(
        max_length=9,
        label="Серия паспорта",
        widget=forms.TextInput(attrs={'placeholder': 'AA1234567'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ""

    class Meta:
        model = User
        fields = ("username", "email", "passport_series", "password1", "password2")

    def clean_passport_series(self):
        data = self.cleaned_data['passport_series']
        pattern = r'^[A-Z]{2}\d{7}$'  # Пример: AA1234567
        if not re.match(pattern, data):
            raise forms.ValidationError(
                "Введите серию паспорта в формате: 2 заглавные буквы и 7 цифр (например, AA1234567)."
            )
        return data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.passport_series = self.cleaned_data["passport_series"]
        if commit:
            user.save()
        return user
