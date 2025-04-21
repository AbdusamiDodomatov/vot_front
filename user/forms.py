from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User  # Только этот импорт нужен!

class RegisterForm(UserCreationForm):
    class Meta:
        model = User  # твоя модель user.User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Логин")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ""  # Убираем описание

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
