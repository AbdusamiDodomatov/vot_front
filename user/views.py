from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Siz tizimga kirdingiz.')
            return redirect('voting:vote_list')
        else:
            messages.error(request, "Noto'g'ri Login yoki parol.")
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Siz tizimdan chiqdingiz.')
    return redirect('login')
