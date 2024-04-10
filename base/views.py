from django.shortcuts import render, redirect
from .models import Event


def home(request):
    events = Event.objects.all()
    
    # Pass the events data to the template
    return render(request, "base/home.html", {'events': events})


def profile(request):
    return render(request, "base/profile.html")


def my_ticket(request):
    return render(request, "base/my-ticket.html")


def payment(request):
    return render(request, "base/payment.html")


def event(request):
    return render(request, "base/event.html")
