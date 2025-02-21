from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


# User Registration
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username is already taken")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email is already registered")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, "Account created successfully!")
                return redirect("login")
        else:
            messages.error(request, "Passwords do not match")

    return render(request, "accounts/register.html")


# User Login
def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")  # Redirect to dashboard after login
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "accounts/login.html")


# User Logout
def user_logout(request):
    logout(request)
    return redirect("login")

def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")  # Redirect logged-in users to dashboard (change as needed)
    return render(request, "accounts/home.html")