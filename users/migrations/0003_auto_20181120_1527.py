# Generated by Django 2.1.3 on 2018-11-20 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_cart'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='cart_id',
            new_name='user',
        ),
    ]
