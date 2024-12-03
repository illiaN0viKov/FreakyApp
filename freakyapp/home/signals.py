from django.db.models.signals import post_migrate, post_save, post_delete
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import *
from chat.models import *

@receiver(post_migrate)
def populate_topics(sender, **kwargs):
    # Add topics if they don't already exist
    for code, name in Topic.TOPIC_CHOICES:
        Topic.objects.get_or_create(name=code)

@receiver(post_save, sender=Event)
def create_chat_group(sender, instance, created, **kwargs):
    if created:
        ChatGroup.objects.create(chat_name=f"{instance.title}", event=instance)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:  
        Profile.objects.create(user=instance)

@receiver(post_delete, sender=ChatGroup)
def handle_chat_deletion(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_discard)(
            async_to_sync(channel_layer.group_send)(
        instance.chat_name,
        {
            "type": "chat_deleted",
            "message": "This chat has been deleted."
        }
    )
        
    )