from django.urls import path
from .views import getTask

urlpatterns = [
    path("", getTask, name="All Task"),
    path("<int:id>", getTask, name="All Task"),
]
