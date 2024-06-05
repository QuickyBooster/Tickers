from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("profile/", views.profile, name="profile"),
    path("my-ticket/", views.my_ticket, name="my-ticket"),
    path("payment/", views.payment, name="payment"),
    path("event/<str:pk>", views.event, name="event"),
    path("login/", views.loginPage, name="login"),
    path("register/", views.registerPage, name="register"),
    path("profile/logout/", views.logoutUser, name="logout"),
]
