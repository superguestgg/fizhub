# Generated by Django 3.2.4 on 2021-10-21 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('physicsesc', '0007_task_picture_href'),
    ]

    operations = [
        migrations.CreateModel(
            name='usefulfiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='no name', max_length=50)),
                ('href', models.CharField(default='no name', max_length=200)),
                ('creator_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='physicsesc.guest')),
            ],
        ),
    ]
