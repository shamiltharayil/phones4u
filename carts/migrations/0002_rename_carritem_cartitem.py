# Generated by Django 4.1.1 on 2022-11-03 00:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Carritem',
            new_name='Cartitem',
        ),
    ]
