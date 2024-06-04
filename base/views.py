from django.shortcuts import render, redirect
from .models import Event, User, Message
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserForm, MyUserCreationForm
from django.contrib import messages
from django.db.models import Min

def home(request):
    # events = Event.objects.all()
    events = Event.objects.annotate(lowest_ticket_price=Min('ticket_types__price'))
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
    message = ""

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        print(username, password)
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "user doesn't exist")
            message = "Failed. Username or Pwd wrong"

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            print("authenticate success!")
            return redirect("home")
        else:
            messages.error(request, "username or password doesn't exist")
    context = {"page": page, "message": message}
    return render(request, "base/login_register.html", context)


def registerPage(request):
    page = "register"
    form = MyUserCreationForm()
    context = {"page": page, "form": form}

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            print("valid form submission")
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            print("???")
            messages.error(request, "An error occurred during registration")

    return render(request, "base/login_register.html", context)


def logoutUser(request):
    logout(request)
    return redirect("home")
