# Generated by Django 5.1.3 on 2024-12-03 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseball_matching', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(blank=True, default='profile_images/default.png', upload_to='profile_images'),
        ),
    ]
