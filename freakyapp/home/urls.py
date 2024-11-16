
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name= "home"),
    path("event/", views.event, name="event"),
    path("profile/", views.profile, name="profile"),

    #for future path of event page
    #path("event/<str:pk>", views.event, name="event")
]
