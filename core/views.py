from django.shortcuts import render
from .mock_data import CURRENT_USER
# Create your views here.

def login(request):
    return render(request, "core/login.html")


def signup(request):
    return render(request, "core/signup.html")


def profile(request):
    return render(request, "core/profile.html", {"current_user": CURRENT_USER})