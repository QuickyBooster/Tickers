from django.shortcuts import render


def home(request):
    return render(request, 'base/home.html')
    return render(request, 'main.html')