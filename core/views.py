from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import LoginForm, ProfileForm, SignupForm
from .models import Profile
from .utils import get_next_url


def login(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        auth.login(request, form.user)
        return redirect(get_next_url(request))
    return render(request, "core/login.html", {"form": form})


def logout(request):
    auth.logout(request)
    return redirect(get_next_url(request))


def signup(request):
    form = SignupForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        auth.login(request, form.save())
        return redirect("index")
    return render(request, "core/signup.html", {"form": form})


@login_required
def profile(request):
    user_profile, _ = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=user_profile)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("profile")
    return render(request, "core/profile.html", {"form": form})
