from django.shortcuts import render, redirect
from .models import Event, User, Message
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserForm, MyUserCreationForm
from django.contrib import messages


def home(request):
    events = Event.objects.all()

    # Pass the events data to the template
    return render(request, "base/home.html", {"events": events})


@login_required(login_url="login")
def profile(request, pk):
    user = User.objects.get(id=pk)
    return render(request, "base/profile.html", {"user": user})


def my_ticket(request):
    return render(request, "base/my-ticket.html")


def payment(request):
    return render(request, "base/payment.html")


def event(request):
    return render(request, "base/event.html")


def loginPage(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "user doesn't exist")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "username or password doesn't exist")
    context = {"page": page}
    return render(request, "base/login_register.html", context)


def registerPage(request):
    page = "register"
    form = MyUserCreationForm()
    context = {"page": page, "form": form}

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error occurred during registration")

    return render(request, "base/login_register.html", context)


def logoutUser(request):
    logout(request)
    return redirect("home")
