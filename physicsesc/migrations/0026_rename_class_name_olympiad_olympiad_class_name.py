# Generated by Django 4.0.2 on 2022-06-14 19:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('physicsesc', '0025_group_group_theme_count_group_theme_group_task'),
    ]

    operations = [
        migrations.RenameField(
            model_name='olympiad',
            old_name='class_name',
            new_name='olympiad_class_name',
        ),
    ]
