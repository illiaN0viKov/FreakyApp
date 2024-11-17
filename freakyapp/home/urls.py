
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name= "home"),
    path("event/", views.event, name="event"),
    path("profile/", views.profile, name="profile"),
    path("login/", views.CustomLogInView.as_view(), name="login"),
    path("logout/", views.CustomLogOutView.as_view(), name="logout"),
    path("success-logout/", views.success_logout, name="success-logout"),
    path("create-event/", views.create_event, name="create-event"),
    path("created-event/", views.event_created, name="event-created"),
    path("registration/", views.registration, name="registration"),
    

    #for future path of event page
    #path("event/<str:pk>", views.event, name="event")
]
