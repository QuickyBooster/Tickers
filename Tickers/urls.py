from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("base.urls"), name="home"),
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
    path("", include("django_prometheus.urls"), name="django-prometheus"),
]
