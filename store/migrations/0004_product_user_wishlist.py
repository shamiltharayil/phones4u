# Generated by Django 4.1.1 on 2022-11-17 17:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0003_reviewrating'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='user_wishlist',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
