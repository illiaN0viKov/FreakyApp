# Generated by Django 4.2.3 on 2024-11-19 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_alter_profile_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(default='default_user.jpg', upload_to='profile/pics/'),
        ),
    ]
