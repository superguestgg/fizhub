# Generated by Django 4.0.2 on 2022-06-12 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('physicsesc', '0021_olympiad_olympiad_part_alter_task_task_text_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='task_type_private',
            field=models.BooleanField(default=False),
        ),
    ]
