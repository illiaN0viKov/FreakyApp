from django.db import models
from django.db.models.signals import post_save
#from django.contrib.auth.models import AbstractUser - here need to specifi authorization in home settings of user will do it later

from django.contrib.auth.models import User


#creating user model
#Integrate user model
'''
class User(AbstractUser):
    name=models.CharField(max_length=200, null=True)
    email=models.EmailField( unique=True, null=True)
    bio=models.TextField(null=True)

    avatar=models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
'''

#creating a room model
class Event(models.Model):
    host=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    

    #think about how to create a topic model
    #topic=models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)


    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    usersJoined=models.ManyToManyField(User, related_name='participants', blank=True) #creating many to mane field connection
    updated=models.DateTimeField(auto_now=True)#(take a time step itself)
             #take a snapshot of any time  model item  was update
    created=models.DateTimeField(auto_now_add=True)#takes a snapshot when firt time create a room

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
    bio = models.TextField(blank=True, null=True)

    def __str__(self) :
          return f"{self.user.username} Profile"


def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance) 
        user_profile.save()
    post_save.connect(create_profile, sender=User)