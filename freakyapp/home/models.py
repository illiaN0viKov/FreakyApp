from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
#from django.contrib.auth.models import AbstractUser - here need to specifi authorization in home settings of user will do it later

from django.contrib.auth.models import User


#creating user model
#Integrate user model

class Topic(models.Model):

    
    TOPIC_CHOICES = [
    ('tech', 'Technology'),
    ('art', 'Art'),
    ('music', 'Music'),
    ('sports', 'Sports'),
    ('education', 'Education'),
    ('football', 'Football'),
    ]

    name = models.CharField(max_length=100, choices=TOPIC_CHOICES)

    def __str__(self):
        return self.name

#creating a room model
class Event(models.Model):
    host=models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="Event Host")
    title = models.CharField(max_length=255,verbose_name="Event Title")
    description = models.TextField(verbose_name="Event Description")
    date = models.DateTimeField(verbose_name="Event Date")
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    maxPeople=models.IntegerField(verbose_name="Maximum People")
    picture= models.ImageField(upload_to='event_pictures/',blank=True, null=True, default='default.jpg')
    topics = models.ManyToManyField(Topic, related_name='events', blank=False)
    participants = models.ManyToManyField(User, related_name="joined_event", blank=True) 
    
   
   
    def __str__(self):
        return f"{self.title} - Event"
    
    def has_space(self):
        return self.participants.count() < self.maxPeople

    def is_user_joined(self, user):
        return self.participants.filter(id=user.id).exists()
    
    



#Chat model
class Chat(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='chats')
    participants = models.ManyToManyField(User, related_name='chat_participations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#message mode
class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_sent')
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=150, blank=True, null=True)
    profile_picture = models.ImageField(null=True, upload_to='profile/pics/', default='default_user.jpg')
    


    def __str__(self) :
          return f"{self.user.username} Profile"

