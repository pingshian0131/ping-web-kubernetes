from django.urls import path

from person.apps import PersonConfig
from person import views

app_name = PersonConfig.name

urlpatterns = [
    path("", views.home, name="home"),
    path("send_email/", views.send_email, name="send_email"),
]
