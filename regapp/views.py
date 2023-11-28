from django.shortcuts import render, redirect
from django.contrib import messages
from . import forms
from django.contrib.auth.decorators import login_required

# Create your views here.


def register(request):
    if request.method == "POST":
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f"{username}, Ваш акаунт було створено, тепер Ви можете увійти")

            return redirect('recipes-home')
    else:
        form = forms.UserRegisterForm()
    return render(request, 'regapp/register.html', {'form': form})


@login_required()
def profile(request):
    return render(request, 'regapp/profile.html')
