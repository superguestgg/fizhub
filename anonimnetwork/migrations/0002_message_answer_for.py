# Generated by Django 3.2.4 on 2021-11-02 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anonimnetwork', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='answer_for',
            field=models.IntegerField(default=0),
        ),
    ]
