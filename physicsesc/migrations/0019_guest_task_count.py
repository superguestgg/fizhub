# Generated by Django 4.0.2 on 2022-06-11 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('physicsesc', '0018_guest_subscriber_count_guest_subscription_count_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='guest',
            name='task_count',
            field=models.IntegerField(default=0),
        ),
    ]