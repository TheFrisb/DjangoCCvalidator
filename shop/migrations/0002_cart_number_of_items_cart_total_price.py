# Generated by Django 4.2.4 on 2023-08-24 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='number_of_items',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='cart',
            name='total_price',
            field=models.IntegerField(default=0),
        ),
    ]
