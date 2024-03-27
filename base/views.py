from django.shortcuts import render



def home(request):
    return render(request, "main-card.html")


def profile(request):
    return render(request, 'event.html')


# def my_ticket(request):
#     return HttpResponse("my_ticket")


# def payment(request):
#     return HttpResponse("payment")


# def event(request):
#     return HttpResponse("event")


# def login(request):
#     return HttpResponse("profile")
