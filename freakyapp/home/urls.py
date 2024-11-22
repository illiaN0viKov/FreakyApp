
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name= "home"),
    path("events/", views.events, name="events"),
    path("profile/", views.profile, name="profile"),
    path('profile/edit/', views.edit_profile, name='edit-profile'),
    path("myEvents/", views.myEvents, name="myEvents"),
    path("login/", views.CustomLogInView.as_view(), name="login"),
    path("logout/", views.CustomLogOutView.as_view(), name="logout"),
    path("success-logout/", views.success_logout, name="success-logout"),
    path("create-event/", views.create_event, name="create-event"),
    path("create-event-topic/", views.create_event_topic, name="create-event-topic"),
    path("created-event/", views.event_created, name="event-created"),
    path('create-event/preview/', views.create_event_preview, name='create-event-preview'),
    path("registration/", views.registration, name="registration"),

    path("edit-event/<str:pk>/", views.editEvent, name="edit-event"),
    path("edit-event-topics/", views.editTopics, name="edit-event-topics"),
    path("edited-event/preview/", views.editPreview, name="edit-event-preview"),
    path("edited-event/", views.editedEvent, name="edited-event"),
    
    path("event-details/<str:pk>/", views.event_details, name="event-details"),
     path('join-event/<str:pk>/', views.join_event, name='join-event'),
]
