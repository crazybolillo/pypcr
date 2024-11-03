from django.urls import path
from . import views

urlpatterns = [
    path("token/<str:key>", views.token),
    path("<str:tenant>/<str:filename>", views.file),
]
