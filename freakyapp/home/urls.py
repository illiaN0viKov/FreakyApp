
from django.contrib import admin
from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name= "home"),
    path("events/", views.events, name="events"),
    path('profile/', views.profile, name='profile'),# This will be used for the current user's profile
    path('profile/edit/', views.edit_profile, name='edit-profile'),
    path("profile/<str:username>/", views.profile, name="profile-other"),
    path("myEvents/", views.myEvents, name="myEvents"), 
    path("login/", views.CustomLogInView.as_view(), name="login"),
    path("logout/", views.CustomLogOutView.as_view(), name="logout"),
    path("success-logout/", views.success_logout, name="success-logout"),

    path("create-event/", views.create_event, name="create-event"),

    path("created-event/", views.event_created, name="event-created"),
    


    path("registration/", views.registration, name="registration"),
    path('calendar/', views.calendar_view, name='calendar'),

    path("edit-event/<str:pk>/", views.editEvent, name="edit-event"),
    
    
    path("delete-event/<str:pk>", views.deleteEvent, name="delete-event"),

    
    path("event-details/<str:pk>/", views.event_details, name="event-details"),
     path('join-event/<str:pk>/', views.join_event, name='join-event'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
