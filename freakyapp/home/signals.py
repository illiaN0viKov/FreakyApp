from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Topic

@receiver(post_migrate)
def populate_topics(sender, **kwargs):
    # Add topics if they don't already exist
    for code, name in Topic.TOPIC_CHOICES:
        Topic.objects.get_or_create(name=code)