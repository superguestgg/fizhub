# Generated by Django 4.0.2 on 2022-03-14 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anonimnetwork', '0005_room_room_type_channel'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='room_channel_admin_password',
            field=models.CharField(default='12345', max_length=50),
        ),
    ]