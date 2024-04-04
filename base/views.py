from django.shortcuts import render


def home(request):
    return render(request, "base/home.html")


def profile(request):
    return render(request, "base/profile.html")


def my_ticket(request):
    return render(request, "base/my-ticket.html")


def payment(request):
    return render(request,"base/payment.html")


def event(request):
    return render(request,"base/event.html")



