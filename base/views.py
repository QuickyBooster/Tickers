from django.shortcuts import render, redirect
from .models import Event, User, Message, Ticket
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserForm, MyUserCreationForm
from django.contrib import messages
from django.db.models import Min


def home(request):
    # events = Event.objects.all()
    events = Event.objects.annotate(lowest_ticket_price=Min("ticket_types__price"))
    # Pass the events data to the template
    return render(request, "base/home.html", {"events": events})


@login_required(login_url="login")
def profile(request):
    user = User.objects.get(id=request.user.id)
    return render(request, "base/profile.html", {"user": user})


@login_required(login_url="login")
def my_ticket(request):
    from datetime import datetime

    today = datetime.today().date()  # Get today's date
    ticket_past = (
        Ticket.objects.filter(user=request.user)
        .exclude(user=None)
        .filter(ticket_type__event__date__lt=today)
    )
    ticket_future = (
        Ticket.objects.filter(user=request.user)
        .exclude(user=None)
        .filter(ticket_type__event__date__gt=today)
    )

    if request.method == "POST":
        ticket_view = request.POST.get("ticket_view")
    else:
        ticket_view = ticket_future.first()

        ticket_list = User.objects.get(id=ticket_view.user.id).ticket_bought.filter(
            ticket_type__event__id=ticket_view.ticket_type.event.id
        )
        total = 0
        for ticket in ticket_list:
            total += ticket.ticket_type.price

    context = {
        "ticket_past": ticket_past,
        "ticket_future": ticket_future,
        "ticket_view": ticket_view,
        "ticket_list": ticket_list,
        "total": total,
    }
    return render(request, "base/my-ticket.html", context)


@login_required(login_url="login")
def payment(request):
    return render(request, "base/payment.html")


def process_payment(payment_id):
    try:
        payment = PendingPayment.objects.get(id=payment_id)
        if payment.status == "Pending":
            payment.status = "Paid"
            payment.save()
            for ticket in payment.tickets.all():
                ticket.user = payment.user
                ticket.save()

            print("Payment processed successfully.")
        else:
            print("Payment already processed.")

    except PendingPayment.DoesNotExist:
        print("Payment not found.")


def event(request, pk):
    event = Event.objects.get(id=pk)
    ticket_types = event.ticket_types.all()
    return render(
        request, "base/event.html", {"event": event, "ticket_types": ticket_types}
    )


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
