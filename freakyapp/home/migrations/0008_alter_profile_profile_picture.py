# Generated by Django 4.2.3 on 2024-11-20 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_alter_profile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(default='pictures/default_user.jpg', null=True, upload_to='profile/pics/'),
        ),
    ]
